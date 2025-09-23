import argparse
import os
from typing import Tuple, List

import numpy as np
import pandas as pd
import torch

# PyG
from torch_geometric.data import Data

# Embeddings
from sentence_transformers import SentenceTransformer

# PCST
import pcst_fast

import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))




def read_kg_csv(input_file):
    """
    Split a knowledge graph CSV file into separate nodes and edges DataFrames.
    
    Args:
        input_file (str): Path to the input CSV file
    """
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where edges section starts
    for i, line in enumerate(lines):
        if line.strip().startswith('src,edge_attr,dst'):
            edge_start_idx = i
            break
    
    # Split into nodes and edges sections
    nodes_lines = lines[:edge_start_idx]
    edges_lines = lines[edge_start_idx:]
    
    # Convert nodes and edges sections to DataFrames
    from io import StringIO
    nodes_str = ''.join(nodes_lines)
    edges_str = ''.join(edges_lines)
    nodes_df = pd.read_csv(StringIO(nodes_str))
    edges_df = pd.read_csv(StringIO(edges_str))
    return nodes_df, edges_df




def load_graph(graph_csv: str) -> Tuple[Data, pd.DataFrame, pd.DataFrame]:
    nodes, edges = read_kg_csv(graph_csv)

    required_nodes = {"node_id", "node_attr"}
    required_edges = {"src", "edge_attr", "dst"}
    if not required_nodes.issubset(nodes.columns):
        raise ValueError(f"nodes.csv missing columns: {required_nodes - set(nodes.columns)}")
    if not required_edges.issubset(edges.columns):
        raise ValueError(f"edges.csv missing columns: {required_edges - set(edges.columns)}")

    # map node_id -> [0..N-1]
    ids = nodes["node_id"].tolist()
    id2idx = {nid: i for i, nid in enumerate(ids)}
    nodes["_idx"] = nodes["node_id"].map(id2idx).astype(int)

    edges["src_idx"] = edges["src"].map(id2idx).astype(int)
    edges["dst_idx"] = edges["dst"].map(id2idx).astype(int)

    edge_index = torch.tensor(np.vstack([edges["src_idx"].to_numpy(), edges["dst_idx"].to_numpy()]), dtype=torch.long)

    data = Data()
    data.num_nodes = len(nodes)
    data.edge_index = edge_index
    return data, nodes, edges




def build_embeddings(nodes: pd.DataFrame, embed_model: str, device: str):
    enc = SentenceTransformer(embed_model, device=device if device != "cpu" else None)
    node_texts = nodes["node_attr"].astype(str).tolist()
    node_emb = enc.encode(node_texts, normalize_embeddings=True, convert_to_numpy=True, batch_size=256, show_progress_bar=True)
    return node_emb, enc




def cosine_topk(matrix: np.ndarray, q: np.ndarray, k: int):
    sims = matrix @ q
    k = min(k, len(sims))
    if k <= 0:
        return  # return empty arraynp.array([], dtype=int), sims
    idx = np.argpartition(-sims, k-1)[:k]
    idx = idx[np.argsort(-sims[idx])]
    return idx, sims




def build_undirected_edges(edge_index_np: np.ndarray):
    src = edge_index_np[0]
    dst = edge_index_np[1]
    undirected = np.vstack([np.minimum(src, dst), np.maximum(src, dst)]).T
    undirected = np.unique(undirected, axis=0)
    costs = np.ones(len(undirected), dtype=np.float64)
    return undirected, costs




def make_prizes(n_nodes: int, node_topk: np.ndarray, sims: np.ndarray, base_prize: float):
    prizes = np.zeros(n_nodes, dtype=np.float64)
    k = len(node_topk)
    for rank, nid in enumerate(node_topk, start=1):
        score = max(0.0, float(sims[nid]))
        prizes[nid] = (k - rank + 1) * base_prize * (0.5 + 0.5 * score)
    return prizes




def pcst(undirected_edges: np.ndarray, prizes: np.ndarray, costs: np.ndarray, root: int = -1, num_clusters: int = 1, pruning: str = "strong"):
    if hasattr(pcst_fast, "pcst"):
        return pcst_fast.pcst(undirected_edges.astype(np.int64), prizes.astype(np.float64), costs.astype(np.float64), root, num_clusters, pruning, 0)
    else:
        return pcst_fast.pcst_fast(undirected_edges.astype(np.int64), prizes.astype(np.float64), costs.astype(np.float64), root, num_clusters, pruning, 0)




def textualize_subgraph(nodes: pd.DataFrame, edges: pd.DataFrame,
                        selected_nodes: np.ndarray,
                        selected_edge_ids: np.ndarray,
                        undirected_edges: np.ndarray) -> str:
    node_lines = [f"[{int(n)}] {nodes.loc[int(n), 'node_attr']}" for n in selected_nodes]

    undirected_set = set(tuple(undirected_edges[e]) for e in selected_edge_ids.tolist())

    edge_lines = []
    for _, row in edges.iterrows():
        u, v = int(row["src_idx"]), int(row["dst_idx"])
        uv = (min(u, v), max(u, v))
        if uv in undirected_set:
            edge_lines.append(f"({u}) -- {row['edge_attr']} --> ({v})")

    return "NODES:\n" + "\n".join(node_lines) + "\n\nEDGES:\n" + "\n".join(edge_lines)




def format_graph_context(textualized_subgraph: str) -> str:
    """
    Converts the textualized subgraph output into a string of edges in the format:
    (NodeA -- Edge -- NodeB)
    """
    # Parse nodes
    node_map = {}
    nodes_section = textualized_subgraph.split("NODES:\n")[1].split("\n\nEDGES:\n")[0].strip().split("\n")
    for line in nodes_section:
        if line.strip():
            idx, attr = line.split("]", 1)
            node_id = int(idx.strip("["))
            node_text = attr.strip()
            node_map[node_id] = node_text

    # Parse edges
    edges_section = textualized_subgraph.split("\n\nEDGES:\n")[1].strip().split("\n")
    formatted_edges = []
    for line in edges_section:
        if line.strip():
            # Example: (0) -- INCLUDES --> (1)
            import re
            match = re.match(r"\((\d+)\) -- ([^>]+) --> \((\d+)\)", line)
            if match:
                src, edge_type, dst = match.groups()
                src_text = node_map.get(int(src), src)
                dst_text = node_map.get(int(dst), dst)
                formatted_edges.append(f"({src_text} -- {edge_type.strip()} -- {dst_text})")

    return "\n".join(formatted_edges)




def retrieve(graph_csv: str, question: str, embed_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
             device: str = "cpu", topk: int = 50, edge_cost: float = 1.0, base_prize: float = 1.0) -> str:
    data, nodes, edges = load_graph(graph_csv)

    node_emb, enc = build_embeddings(nodes, embed_model, device)

    q_vec = enc.encode([question], normalize_embeddings=True, convert_to_numpy=True)[0]
    node_topk, sims = cosine_topk(node_emb, q_vec, topk)

    undirected_edges, undirected_costs = build_undirected_edges(data.edge_index.numpy())

    undirected_costs = np.full_like(undirected_costs, edge_cost, dtype=np.float64)

    prizes = make_prizes(data.num_nodes, node_topk, sims, base_prize)

    selected_nodes, selected_edge_ids = pcst(undirected_edges, 
                                             prizes, 
                                             undirected_costs, 
                                             root=-1, num_clusters=1, pruning="strong")

    ctx = textualize_subgraph(nodes, edges, 
                              selected_nodes, selected_edge_ids, 
                              undirected_edges)

    formatted_context = format_graph_context(ctx)
    return formatted_context


