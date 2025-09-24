import re
from rdflib import Graph, RDF, OWL, RDFS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from pyvis.network import Network

from langchain_openai import AzureChatOpenAI
import os
from app_settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_DEPLOYMENT_GPT41_NANO
)

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
    # Ensure relative paths are resolved from PROJECT_ROOT
    import os
    from app_settings import PROJECT_ROOT
    if not os.path.isabs(ttl_file_path):
        ttl_file_path = os.path.join(PROJECT_ROOT, ttl_file_path)
    # Convert to file URI for rdflib
    file_uri = os.path.abspath(ttl_file_path).replace('\\', '/')
    g = Graph()
    g.parse(file_uri, format="turtle")
    
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




def chunk_document(document, chunk_size=1500, chunk_overlap=50):
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
    
    # Handle empty input
    if not graph_documents:
        print("merge_graph_documents: input list is empty, returning []")
        return []
    
    # Create merged document
    merged_doc = type(graph_documents[0])( 
        nodes=unique_nodes,
        relationships=unique_relationships,
        source=graph_documents[0].source
    )
    print(f"Merged: {len(unique_nodes)} nodes, {len(unique_relationships)} relationships")
    return [merged_doc]


def merge_graph_documents_with_chunks(graph_documents):
    """Merge graph documents while preserving chunk information as nodes in the graph."""
    from langchain_community.graphs.graph_document import Node, Relationship
    
    all_nodes = []
    all_relationships = []
    chunk_nodes = []
    
    # Add chunk nodes and track relationships between entities and chunks
    for i, doc in enumerate(graph_documents):
        # Create a node representing this chunk
        chunk_id = f"Chunk_{i}: "
        chunk_node = Node(
            id=chunk_id,
            type="TextChunk",
            properties={
                "content": doc.source.page_content,  
                "chunk_index": i,
                "metadata": str(doc.source.metadata) if hasattr(doc.source, "metadata") else "{}"
            }
        )
        chunk_nodes.append(chunk_node)
        all_nodes.append(chunk_node)
        
        # Add all nodes from this chunk
        all_nodes.extend(doc.nodes)
        
        # Add relationships between chunk and its nodes
        for node in doc.nodes:
            all_relationships.append(
                Relationship(
                    source=chunk_node,
                    target=node,
                    type="CONTAINS_ENTITY"
                )
            )
        
        # Add all relationships from this chunk
        all_relationships.extend(doc.relationships)
    
    # Remove duplicate nodes by ID (keeping the first occurrence)
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
    
    # Handle empty input
    if not graph_documents:
        print("merge_graph_documents_with_chunks: input list is empty, returning []")
        return []
    
    # Create merged document
    merged_doc = type(graph_documents[0])( 
        nodes=unique_nodes,
        relationships=unique_relationships,
        source=graph_documents[0].source
    )
    
    print(f"Merged: {len(unique_nodes)} nodes ({len(chunk_nodes)} chunk nodes), {len(unique_relationships)} relationships")
    return [merged_doc]


def visualize_graph(graph_documents, output_file = "knowledge_graph.html"):
    """
    Code from https://github.com/thu-vu92/knowledge-graph-llms/tree/main
    """
    if not graph_documents:
        print("No graph documents to visualize. Skipping visualization.")
        return

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
    print(f"HTML visualization: {os.path.abspath(output_file)}")

    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(output_file)}")
    except:
        print("Could not open browser automatically")


def visualize_graph_with_chunks(graph_documents, output_file = "knowledge_graph.html"):
    """
    Visualize graph documents with special styling for chunk nodes.
    """
    if not graph_documents:
        print("No graph documents to visualize. Skipping visualization.")
        return

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

    # Add valid nodes with special styling for chunks
    for node_id in valid_node_ids:
        node = node_dict[node_id]
        try:
            # Check if node is a chunk
            is_chunk = hasattr(node, 'type') and node.type == "TextChunk"
            
            # Get content preview for chunks
            content_preview = ""
            if is_chunk and hasattr(node, 'properties') and node.properties:
                content_preview = node.properties.get("content", "")
            
            # Create detailed tooltip
            tooltip = f"Type: {node.type}<br>"
            if content_preview:
                tooltip += f"Content: {content_preview}<br>"
            
            # Add node with appropriate styling
            if is_chunk:
                # Chunks get special styling - larger, different shape, different color
                net.add_node(
                    node.id, 
                    label=node.id, 
                    title=tooltip,
                    shape="diamond",  # Different shape for chunks
                    color="#BB0000",  # Red color for chunks
                    size=25,          # Larger size
                    group="Chunk"     # Group all chunks together
                )
            else:
                # Regular entity nodes
                net.add_node(
                    node.id, 
                    label=node.id, 
                    title=tooltip, 
                    group=node.type
                )
        except Exception as e:
            print(f"Error adding node {node.id}: {e}")
            continue  # skip if error

    # Add valid edges with special styling for chunk relationships
    for rel in valid_edges:
        try:
            # Check if this is a chunk relationship
            is_chunk_rel = (
                rel.type == "CONTAINS_ENTITY" or 
                (hasattr(rel.source, 'type') and rel.source.type == "TextChunk") or
                (hasattr(rel.target, 'type') and rel.target.type == "TextChunk")
            )
            
            if is_chunk_rel:
                # Chunk relationships get dashed lines and different color
                net.add_edge(
                    rel.source.id, 
                    rel.target.id, 
                    label=rel.type.lower(),
                    dashes=True,
                    color="#BB0000"  # Red for chunk relationships
                )
            else:
                # Regular relationships
                net.add_edge(
                    rel.source.id, 
                    rel.target.id, 
                    label=rel.type.lower()
                )
        except Exception as e:
            print(f"Error adding edge {rel.source.id} -> {rel.target.id}: {e}")
            continue  # skip if error

    # Configure physics - cluster chunks and their entities
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
            },
            "edges": {
                "smooth": {
                    "type": "continuous",
                    "forceDirection": "none"
                }
            },
            "interaction": {
                "hover": true,
                "navigationButtons": true,
                "keyboard": true
            }
        }
        """)
    
    net.save_graph(output_file)
    print(f"HTML visualization: {os.path.abspath(output_file)}")

    # Try to open in browser
    try:
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(output_file)}")
    except:
        print("Could not open browser automatically")



def save_graph_to_csv(graph_documents, output_file="."):
    """
    Save the graph as two CSV files: nodes and edges, in the specified directory.

    Args:
        graph_documents: List of graph documents (as produced by LLMGraphTransformer)
        output_file: Directory to save the nodes and edges CSV files
    """
    import os

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
    csv_data.append("node_id,node_attr,node_type") 

    # Add nodes with their attributes
    for node in nodes:
        node_id = node_id_mapping[node.id]
        
        # Check if this is a chunk node
        is_chunk = hasattr(node, 'type') and node.type == "TextChunk"
        
        # Get node type
        node_type = node.type if hasattr(node, 'type') and node.type else "Unknown" 
        
        # Format node attribute
        node_attr = f"{node.id}"
        
        # Get properties as JSON string
        properties = ""
        if hasattr(node, 'properties') and node.properties:
            import json
            if is_chunk and 'content' in node.properties:
                node_properties = node.properties.copy()
                properties = json.dumps(node_properties['content'])
            else:
                continue

        csv_data.append(f'{node_id},"{node_attr + properties.replace('"', "'")}","{node_type}"') 

    # Add empty line separator
    csv_data.append("")
    
    # Add header for edges section
    csv_data.append("src,edge_attr,dst,is_chunk_relation")

    # Add edges
    for rel in relationships:
        src_id = node_id_mapping.get(rel.source.id)
        dst_id = node_id_mapping.get(rel.target.id)
        if src_id is None or dst_id is None:
            continue
        edge_attr = rel.type
        
        # Check if this is a chunk relationship
        is_chunk_rel = (
            rel.type == "CONTAINS_ENTITY" or 
            (hasattr(rel.source, 'type') and rel.source.type == "TextChunk") or
            (hasattr(rel.target, 'type') and rel.target.type == "TextChunk")
        )
        
        csv_data.append(f'{src_id},"{edge_attr}",{dst_id},{1 if is_chunk_rel else 0}')

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(csv_data))
    
    print(f"Graph saved to: {os.path.abspath(output_file)}")
    print(f"Total nodes: {len(nodes)}")
    print(f"Total edges: {len(relationships)}")
    
    # Count chunk nodes
    chunk_nodes = [n for n in nodes if hasattr(n, 'type') and n.type == "TextChunk"]
    print(f"Chunk nodes: {len(chunk_nodes)}")
    
    # Count chunk relationships
    chunk_rels = [r for r in relationships if 
                 r.type == "CONTAINS_ENTITY" or 
                 (hasattr(r.source, 'type') and r.source.type == "TextChunk") or
                 (hasattr(r.target, 'type') and r.target.type == "TextChunk")]
    print(f"Chunk relationships: {len(chunk_rels)}")



async def abuild_kg(
    input_path: str,
    ontology_path: str = None,
    html_output: str = "knowledge_graph.html",
    include_chunks: bool = False,
    chunk_size: int = 3000,
    chunk_overlap: int = 50,
    visualize: bool = True,
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
    # --- Improved error handling and diagnostics ---

    # --- Early validations ---
    print(f"Input path: {input_path}")
    if not input_path or not isinstance(input_path, str):
        raise ValueError("Input path must be a non-empty string.")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    if not (os.path.isfile(input_path) or os.path.isdir(input_path)):
        raise ValueError(f"Input path must be a file or directory: {input_path}")

    if ontology_path:
        if not os.path.exists(ontology_path):
            print(f"Warning: Ontology path does not exist: {ontology_path}")
        # No need to raise, just warn

    # Validate output directory for html_output (if visualize)
    if visualize:
        output_dir = os.path.dirname(html_output)
        if output_dir and not os.path.exists(output_dir):
            raise FileNotFoundError(f"Output directory does not exist for html_output: {output_dir}")

    # Extract ontology constraints if provided
    classes = None
    relations = None
    if ontology_path and os.path.exists(ontology_path):
        try:
            print("Ontology path exists")
            classes, relations, attributes = extract_local_names(ontology_path)
            print(f"Using ontology constraints: {len(classes)} classes, {len(relations)} relations")
        except Exception as e:
            print(f"Warning: Could not load ontology from {ontology_path}: {e}")
            print("Proceeding without ontology constraints...")

    # Read input
    content = ""
    if os.path.isfile(input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                content = file.read()
            print(f"Loaded content from {input_path}")
            if not content.strip():
                raise ValueError(f"Input file is empty: {input_path}")
        except Exception as e:
            print(f"Error reading file {input_path}: {e}")
            raise
    elif os.path.isdir(input_path):
        txt_files = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        if not txt_files:
            raise FileNotFoundError(f"No .txt files found in directory: {input_path}")
        for filename in txt_files:
            file_path = os.path.join(input_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    if not file_content.strip():
                        print(f"Warning: {filename} is empty.")
                    content += file_content + "\n\n"
                print(f"Loaded content from {filename}")
            except Exception as e:
                print(f"Warning: Error reading {filename}: {e}")
        if not content.strip():
            raise ValueError(f"All .txt files in directory are empty: {input_path}")

    # Process content
    document = Document(page_content=content)
    chunks = chunk_document(document, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    print(f"Split into {len(chunks)} chunks")

    # Create graph transformer
    if not classes or not relations:
        print("No ontology constraints provided or loaded")

    # allowed_relationships = [
    #     (source_class, relation, target_class) 
    #     for source_class in classes 
    #     for target_class in classes 
    #     for relation in relations
    # ]
    additional_instructions = (
    "Extract all possible relationships from the text:\n"
    "1. Direct (explicit) relationships\n"
    "2. Implicit relationships that can be reasonably inferred\n"
    "3. Secondary and subtle relationships between entities\n\n"
    "Requirements:\n"
    "- Use ENGLISH for all nodes, relationships, and properties.\n"
    "- Group very similar concepts together.\n"
    "- Use allowed_nodes as first-level entities; create second-level entities as needed, linking each to a first-level entity.\n"
    "- For each entity, extract at least 2 connections.\n"
    "- Ensure every node connects to at least one other node."
    )
    
    transformer_kwargs = {
        "llm": gpt41_nano,
        "allowed_nodes": classes,
        "allowed_relationships": relations,
        "ignore_tool_usage": False, # bypass the use of structured output (False by default)
        # If ignore_tool_usage is True, then node_properties and relationship_properties must be False
        "node_properties": False, # LLM can extract any node properties from text (False by default)
        "relationship_properties": False, # LLM can extract any relationship properties from text (False by default)
        "strict_mode": False, # Only use allowed nodes/relationships (True by default)
        "additional_instructions": additional_instructions
    }
        
    graph_transformer = LLMGraphTransformer(**transformer_kwargs)

    # Convert to graph
    print("Converting text to graph documents...")
    graph_documents = await graph_transformer.aconvert_to_graph_documents(chunks)
    
    # Merge documents
    if include_chunks:
        print("Merging documents while preserving chunk information...")
        graph_documents = merge_graph_documents_with_chunks(graph_documents)
    else:
        print("Merging documents...")
        graph_documents = merge_graph_documents(graph_documents)
        
    if not graph_documents:
        print("No graph documents generated. Exiting.")
        return []

    if visualize:
        if include_chunks:
            print("Visualizing graph with chunks...")
            visualize_graph_with_chunks(graph_documents, output_file=html_output)
        else:
            print("Visualizing graph...")
            visualize_graph(graph_documents, output_file=html_output)

    print(f"Knowledge graph built successfully!")
    
    return graph_documents


# ---------------------------------- RUNNING ----------------------------------


async def main():
    classes, relations, attributes = extract_local_names('results/ontologies/rdb/rigor_ontology_few_fixes.ttl')

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

    save_graph_to_csv(graph_documents, output_file="results/kgs/rdb_ontology_aligned_KG.csv")



#if __name__ == "__main__":
#    asyncio.run(main())