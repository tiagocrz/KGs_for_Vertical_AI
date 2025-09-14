import re
from rdflib import Graph, RDF, OWL, RDFS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from pyvis.network import Network

import asyncio

from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

AZURE_DEPLOYMENT_GPT41 = os.getenv("AZURE_DEPLOYMENT_GPT41")
AZURE_DEPLOYMENT_GPT41_NANO = os.getenv("AZURE_DEPLOYMENT_GPT41_NANO")

gpt41_nano = AzureChatOpenAI(
    azure_deployment=AZURE_DEPLOYMENT_GPT41_NANO,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    temperature=0
)


# ---------------------------------- TOOLS ----------------------------------


def extract_ontology_lexical_view(ontology_path: str) -> list:
    """
    Returns format: ['label: comment', 'label2: comment2']
    Pairs labels with their corresponding comments
    """
    with open(ontology_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lexical_view = []
    
    # Find all rdfs:label and rdfs:comment matches with their positions
    label_pattern = r'rdfs:label\s+"([^"]+)"'
    comment_pattern = r'rdfs:comment\s+"([^"]+)"'
    
    # Get all matches in order
    labels = [match.group(1).replace(" ", "") for match in re.finditer(label_pattern, content)]
    comments = [match.group(1) for match in re.finditer(comment_pattern, content)]

    # Pair them sequentially (comment[i] goes with label[i])
    for i in range(len(labels)):
        if i < len(comments):
            lexical_view.append(f"{labels[i]}: {comments[i]}")
        else:
            lexical_view.append(f"{labels[i]}: ")
    
    return lexical_view




def extract_local_names(ttl_file_path):
    """
    Extract ontology elements (local names without full URIs).
    Returns:
        - class_names: ontology classes (entities)
        - object_property_names: ontology object properties (relationships)
        - datatype_property_names: ontology datatype properties (attributes)
    """
    g = Graph()
    g.parse(ttl_file_path, format="turtle")
    
    def get_local_name(uri):
        uri_str = str(uri)
        if '#' in uri_str: 
            return uri_str.split('#')[-1]
        return uri_str.split('/')[-1]
    
    # Classes
    #class_uris = [s for s, _, _ in g.triples((None, RDF.type, OWL.Class))]
    class_uris = set(
    [s for s, _, _ in g.triples((None, RDF.type, OWL.Class))] +
    [s for s, _, _ in g.triples((None, RDF.type, RDFS.Class))]
)

    class_names = [get_local_name(uri) for uri in class_uris]
    
    # Object properties
    object_prop_uris = [s for s, _, _ in g.triples((None, RDF.type, OWL.ObjectProperty))]
    object_prop_uris = set(
    [s for s, _, _ in g.triples((None, RDF.type, OWL.ObjectProperty))] +
    [s for s, _, _ in g.triples((None, RDF.type, RDF.Property))]
)

    object_property_names = [get_local_name(uri) for uri in object_prop_uris]
    
    # Datatype properties
    data_prop_uris = [s for s, _, _ in g.triples((None, RDF.type, OWL.DatatypeProperty))]
    datatype_property_names = [get_local_name(uri) for uri in data_prop_uris]
    
    return (
        sorted(class_names),
        sorted(object_property_names),
        sorted(datatype_property_names),
    )




def chunk_document(document, chunk_size=3000, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents([document])




def merge_graph_documents(graph_documents):
    """Simple function to merge all nodes and relationships from graph documents."""

    all_nodes = []
    all_relationships = []
    
    # Collect everything
    for doc in graph_documents:
        all_nodes.extend(doc.nodes)
        all_relationships.extend(doc.relationships)
    
    # Remove duplicate nodes by ID
    seen_nodes = set()
    unique_nodes = []
    for node in all_nodes:
        if node.id not in seen_nodes:
            seen_nodes.add(node.id)
            unique_nodes.append(node)
    
    # Remove duplicate relationships
    seen_rels = set()
    unique_relationships = []
    for rel in all_relationships:
        rel_key = (rel.source.id, rel.target.id, rel.type)
        if rel_key not in seen_rels:
            seen_rels.add(rel_key)
            unique_relationships.append(rel)
    
    # Create merged document
    merged_doc = type(graph_documents[0])(
        nodes=unique_nodes,
        relationships=unique_relationships,
        source=graph_documents[0].source
    )
    
    print(f"Merged: {len(unique_nodes)} nodes, {len(unique_relationships)} relationships")
    return [merged_doc]




def visualize_graph(graph_documents, output_file = "knowledge_graph.html"):
    """
    Code from https://github.com/thu-vu92/knowledge-graph-llms/tree/main
    """

    # Create network
    net = Network(height="1200px", width="100%", directed=True,
                      notebook=False, bgcolor="#222222", font_color="white")
    
    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships

    # Build lookup for valid nodes
    node_dict = {node.id: node for node in nodes}
    
    # Filter out invalid edges and collect valid node IDs
    valid_edges = []
    valid_node_ids = set()
    for rel in relationships:
        if rel.source.id in node_dict and rel.target.id in node_dict:
            valid_edges.append(rel)
            valid_node_ids.update([rel.source.id, rel.target.id])


    # Track which nodes are part of any relationship
    connected_node_ids = set()
    for rel in relationships:
        connected_node_ids.add(rel.source.id)
        connected_node_ids.add(rel.target.id)

    # Add valid nodes
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            net.add_node(node.id, label=node.id, title=node.type, group=node.type)
        except:
            continue  # skip if error

    # Add valid edges
    for rel in valid_edges:
        try:
            net.add_edge(rel.source.id, rel.target.id, label=rel.type.lower())
        except:
            continue  # skip if error

    # Configure physics
    net.set_options("""
            {
                "physics": {
                    "forceAtlas2Based": {
                        "gravitationalConstant": -100,
                        "centralGravity": 0.01,
                        "springLength": 200,
                        "springConstant": 0.08
                    },
                    "minVelocity": 0.75,
                    "solver": "forceAtlas2Based"
                }
            }
            """)
        
    net.save_graph(output_file)
    print(f"Graph saved to {os.path.abspath(output_file)}")

    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(output_file)}")
    except:
        print("Could not open browser automatically")




def save_graph_to_csv(graph_documents, output_file="graph.csv"):
    nodes = graph_documents[0].nodes
    relationships = graph_documents[0].relationships
    
    # Create a mapping from node IDs to sequential integers
    node_id_mapping = {}
    sequential_id = 1
    
    for node in nodes:
        if node.id not in node_id_mapping:
            node_id_mapping[node.id] = sequential_id
            sequential_id += 1
    
    # Prepare data for CSV
    csv_data = []
    
    # Add header for nodes section
    csv_data.append("node_id,node_attr")
    
    # Add nodes with their attributes
    for node in nodes:
        node_id = node_id_mapping[node.id]
        # Format: "Type: NodeName" or just "NodeName" if no type
        if hasattr(node, 'type') and node.type:
            node_attr = f"{node.type}: {node.id}"
        else:
            node_attr = node.id
        
        csv_data.append(f'{node_id},"{node_attr}"')
    
    # Add empty line separator
    csv_data.append("")
    
    # Add header for edges section
    csv_data.append("src,edge_attr,dst")
    
    # Add edges
    for rel in relationships:
        src_id = node_id_mapping.get(rel.source.id)
        dst_id = node_id_mapping.get(rel.target.id)
        
        # Skip if either node ID is not found
        if src_id is None or dst_id is None:
            continue
            
        edge_attr = rel.type
        csv_data.append(f'{src_id},"{edge_attr}",{dst_id}')
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(csv_data))
    
    print(f"Graph saved to: {os.path.abspath(output_file)}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Total edges: {len(relationships)}")




async def abuild_kg(
    input_path: str,
    ontology_path: str = None,
    chunk_size: int = 3000,
    chunk_overlap: int = 50,
    visualize: bool = True,
    html_output: str = "knowledge_graph.html"
):
    """
    Build a knowledge graph from input text file(s).
    
    Args:
        input_path (str): Path to input text file or folder containing text files
        ontology_path (str, optional): Path to ontology TTL file for constraints
        chunk_size (int): Size of text chunks for processing (default: 3000)
        chunk_overlap (int): Overlap between chunks (default: 50)
        visualize (bool): Whether to create HTML visualization (default: True)
        html_output (str): Path for HTML visualization file (default: "knowledge_graph.html")
    
    Returns:
        tuple: (graph_documents, node_id_mapping)
    """
    # Initialize empty classes and relations
    classes = None
    relations = None
    print(f"Input path: {input_path}") # remove

    # Extract ontology constraints if provided    
    if ontology_path and os.path.exists(ontology_path):
        try:
            print("Path exists") # remove
            classes, relations, attributes = extract_local_names(ontology_path)
            print(f"Using ontology constraints: {len(classes)} classes, {len(relations)} relations")
        except Exception as e:
            print(f"Warning: Could not load ontology from {ontology_path}: {e}")
            print("Proceeding without ontology constraints...")

    # Read input
    content = ""
    if os.path.isfile(input_path): # Single file
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print(f"Loaded content from {input_path}")
        except Exception as e:
            raise Exception(f"Error reading file {input_path}: {e}")
            
    elif os.path.isdir(input_path): # Directory - process all .txt files
        txt_files = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        if not txt_files:
            raise Exception(f"No .txt files found in {input_path}")
            
        for filename in txt_files:
            file_path = os.path.join(input_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content += file.read() + "\n\n"
                print(f"Loaded content from {filename}")
            except Exception as e:
                print(f"Warning: Error reading {filename}: {e}")

    # Process content
    document = Document(page_content=content)
    chunks = chunk_document(document, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print(f"Split into {len(chunks)} chunks")

    # Create graph transformer
    transformer_kwargs = {"llm": gpt41_nano}
    print("Classes:", classes) # remove
    print("Relations:", relations) # remove
    if classes:
        transformer_kwargs["allowed_nodes"] = classes
    if relations:
        transformer_kwargs["allowed_relationships"] = relations
    transformer_kwargs["ignore_tool_usage"] = True # try without
    # transformer_kwargs["node_properties"] = True
    # transformer_kwargs["relationship_properties"] = True

    print("Graph transformer settings:", transformer_kwargs) # remove
        
    graph_transformer = LLMGraphTransformer(**transformer_kwargs)

    # Convert to graph
    print("Converting text to graph documents...")
    graph_documents = await graph_transformer.aconvert_to_graph_documents(chunks)

    for graph in graph_documents: # remove
        print(f"Graph document: {(graph.nodes)} nodes, {(graph.relationships)} relationships. Document: {graph.source.page_content[:25]}...") # remove
    
    # Merge documents
    graph_documents = merge_graph_documents(graph_documents)

    if visualize:
        visualize_graph(graph_documents, output_file=html_output)

    print(f"Knowledge graph built successfully!")
    if visualize:
        print(f"HTML visualization: {os.path.abspath(html_output)}")
    
    return graph_documents


# ---------------------------------- RUNNING ----------------------------------


async def main():
    classes, relations, attributes = extract_local_names('results/ontologies/RDB/rigor_ontology_few_fixes.ttl')

    input_txt_folder = "data/texts"
    for filename in os.listdir(input_txt_folder):
        if filename.endswith('opportunity_example.txt'):
            file_path = os.path.join(input_txt_folder, filename)
            print(f"Processing {filename}...")

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
            except Exception as e:
                print(f"Error processing {filename}: {e}")


    document = Document(page_content=content)
    chunks = chunk_document(document)

    graph_transformer = LLMGraphTransformer(llm = gpt41_nano,
                                        allowed_nodes = classes,
                                        allowed_relationships=relations.remove('relatesToTable'))
    
    
    graph_documents = await graph_transformer.aconvert_to_graph_documents(chunks)

    graph_documents = merge_graph_documents(graph_documents)

    visualize_graph(graph_documents, 'src/knowledge_graph')

    save_graph_to_csv(graph_documents, output_file="results/KGs/rdb_ontology_aligned_KG.csv")



#if __name__ == "__main__":
#    asyncio.run(main())