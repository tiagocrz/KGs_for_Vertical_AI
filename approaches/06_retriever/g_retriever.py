# ===== 0) imports & config =====
import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.llm.models import GRetriever  # PyG's built-in retriever
from sentence_transformers import SentenceTransformer
from pcst_fast import pcst_fast  # Prize-Collecting Steiner Tree (PCST)

# choose a compact, fast embedder (normalized cos-sim ready)
EMBED_MODEL = "all-MiniLM-L6-v2"   # change if you want
st = SentenceTransformer(EMBED_MODEL)

# -------- Optional: keep your AzureChatOpenAI via a tiny adapter ----------
# If you already have: from langchain_openai import AzureChatOpenAI
USE_AZURE = False
if USE_AZURE:
    from langchain_openai import AzureChatOpenAI
    azure_llm = AzureChatOpenAI(
        azure_deployment="gpt-4o-mini",  # your deployment name
        api_version="2024-XX-XX"
    )
    class AzureLLMAdapter(torch.nn.Module):
        def __init__(self, m): super().__init__(); self.m = m
        def forward(self, prompt: str, **kw): return self.m.invoke(prompt)
    LLM_BACKEND = AzureLLMAdapter(azure_llm)
else:
    # simple echo for smoke tests; replace with your HF/Azure model later
    class Echo(torch.nn.Module):
        def forward(self, prompt, **kw): return "[ECHO] " + prompt[:300]
    LLM_BACKEND = Echo()

# ===== 1) load KG (CSV -> in-memory) =====
def load_kg(nodes_csv: str, edges_csv: str):
    nodes = pd.read_csv(nodes_csv)           # cols: node_id,node_attr
    edges = pd.read_csv(edges_csv)           # cols: src,edge_attr,dst
    # assure types
    nodes["node_id"] = nodes["node_id"].astype(int)
    edges["src"] = edges["src"].astype(int)
    edges["dst"] = edges["dst"].astype(int)
    return nodes, edges

# ===== 2) build PyG Data with text features =====
def build_graph(nodes: pd.DataFrame, edges: pd.DataFrame) -> tuple[Data, list[str], list[str]]:
    """
    - x: node text embeddings
    - edge_attr: edge text embeddings
    - keep raw text for prompting (node_text, edge_text)
    """
    # map node_id -> 0..N-1
    id2idx = {nid: i for i, nid in enumerate(nodes["node_id"].tolist())}
    N = len(id2idx)

    # edge_index
    src = edges["src"].map(id2idx).to_numpy()
    dst = edges["dst"].map(id2idx).to_numpy()
    edge_index = torch.tensor([src, dst], dtype=torch.long)

    # texts
    node_text = nodes["node_attr"].astype(str).tolist()
    edge_text = edges["edge_attr"].astype(str).tolist()

    # embeddings (unit-normalized by the model when we set normalize below)
    x = torch.tensor(st.encode(node_text, normalize_embeddings=True), dtype=torch.float)
    e = torch.tensor(st.encode(edge_text, normalize_embeddings=True), dtype=torch.float)

    data = Data(x=x, edge_index=edge_index, edge_attr=e)
    data.node_text = node_text
    data.edge_text = edge_text
    data.id2idx = id2idx
    return data, node_text, edge_text

# ===== 3) PCST retrieval (scores -> connected subgraph) =====
@torch.no_grad()
def retrieve_pcst_subgraph(question: str, data: Data, k_seeds: int = 25,
                           prize_scale: float = 1.0, cost_scale: float = 1.0) -> Data:
    # (a) question embedding (unit norm)
    q = torch.tensor(st.encode([question], normalize_embeddings=True)[0], dtype=torch.float)  # [d]

    # (b) node prizes = positive cosine with q
    prizes = torch.mv(data.x, q).clamp(min=0.0).cpu().numpy() * prize_scale

    # (c) edge costs = 1 - positive cosine with q
    e_sims = torch.mv(data.edge_attr, q).clamp(min=0.0).cpu().numpy()
    costs = (1.0 - e_sims * cost_scale)

    # (d) undirected edge list for PCST (use both directions or unique pairs)
    edges_undirected = data.edge_index.t().cpu().tolist()

    # (e) seed terminals = top-k prize nodes
    import numpy as np
    k = min(k_seeds, len(prizes))
    terminals = np.argpartition(-prizes, kth=k-1)[:k].tolist()

    keep_nodes, keep_edges = pcst_fast(
        edges=edges_undirected,
        prizes=prizes.tolist(),
        costs=costs.tolist(),
        root=None, g='s', pruning='gw', verbosity_level=0
    )

    # (f) mask and remap
    keep_nodes = sorted(set(keep_nodes) | set(terminals))
    node_mask = torch.zeros(data.num_nodes, dtype=torch.bool); node_mask[keep_nodes] = True
    edge_mask = torch.zeros(data.num_edges, dtype=torch.bool)
    for ei in keep_edges: edge_mask[ei] = True

    def remap(edge_index, mask):
        old2new = -torch.ones(mask.size(0), dtype=torch.long)
        old2new[mask] = torch.arange(mask.sum())
        return old2new[edge_index]

    sub = Data(
        x=data.x[node_mask],
        edge_index=remap(data.edge_index[:, edge_mask], node_mask),
        edge_attr=data.edge_attr[edge_mask],
    )
    sub.node_text = [data.node_text[i] for i in keep_nodes]
    sub.edge_text = [data.edge_text[i] for i, m in enumerate(edge_mask.tolist()) if m]
    return sub

# ===== 4) Prompt construction =====
def make_prompt(question: str, sub: Data) -> str:
    lines = ["You are a helpful assistant that answers using ONLY the provided subgraph.",
             "Cite nodes/edges if relevant.",
             "", "# Subgraph"]
    lines += [f"- NODE: {t}" for t in getattr(sub, "node_text", [])]
    lines += [f"- EDGE: {t}" for t in getattr(sub, "edge_text", [])]
    lines += ["", f"Q: {question}", "A:"]
    return "\n".join(lines)

# ===== 5) Ask with GRetriever (wraps LLM; GNN optional) =====
def answer_question(question: str, data: Data):
    sub = retrieve_pcst_subgraph(question, data)
    prompt = make_prompt(question, sub)
    model = GRetriever(llm=LLM_BACKEND, gnn=None, use_lora=False)  # keep it light; plug a GNN later if you want
    return model(prompt), sub

# ===== 6) Run end-to-end =====
if __name__ == "__main__":
    nodes, edges = load_kg("nodes.csv", "edges.csv")
    data, _, _ = build_graph(nodes, edges)

    question = "Quem financia o projecto 'Agente de IA'?"  # example in PT just to show it works with any text
    answer, sub = answer_question(question, data)

    print(f"Subgraph → {sub.num_nodes} nodes, {sub.num_edges} edges")
    print("Answer:\n", answer)
