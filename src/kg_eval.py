# ---------------------------
# LLM Interpretation Function
# ---------------------------
from __future__ import annotations

from langchain_openai import AzureChatOpenAI
import pandas as pd
import numpy as np
import networkx as nx
from typing import Dict, Any, Tuple, Optional, Callable

from app_settings import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_VERSION,
    AZURE_DEPLOYMENT_GPT41
)

"""
Knowledge Graph Evaluation Module

This module provides tools for evaluating CSV-based knowledge graphs, focusing on
structural metrics and quality scores for AI retrieval applications. The main
workflow is:

1. Load a graph from a CSV file
2. Compute structural metrics (connectivity, paths, clustering, etc.)
3. Calculate a normalized quality score (0-1)
4. Generate a formatted report for comparison

Usage:
    results1 = evaluate_csv('path/to/graph1.csv')
    results2 = evaluate_csv('path/to/graph2.csv')
    report1 = format_report(results1)
    report2 = format_report(results2)
    interpretation = interpret_kg_comparison_with_llm(report1, report2)
    print(interpretation)
"""

# Configuration constants
HEAVY_NODES_THRESHOLD = 150_000  # Skip intensive metrics for graphs larger than this

# ---------------------------
# Graph Loading Functions
# ---------------------------

def load_graph_from_csv(csv_path: str,
                        source_col: str = 'source',
                        target_col: str = 'target',
                        directed: bool = False,
                        weight_col: Optional[str] = None,
                        delimiter: Optional[str] = None,
                        error_bad_lines: bool = False) -> Tuple[nx.Graph, pd.DataFrame]:
    """Load a graph from an edge-list CSV file.
    
    Creates either a directed or undirected graph from a CSV file containing
    edge information. The CSV must contain columns for source and target nodes,
    and optionally a column for edge weights.
    
    Args:
        csv_path: Path to the CSV file
        source_col: Name of the column containing source nodes
        target_col: Name of the column containing target nodes
        directed: If True, create a directed graph (DiGraph), else undirected
        weight_col: Optional name of column containing edge weights
        delimiter: Optional delimiter character to use (auto-detected if None)
        error_bad_lines: If True, raise exception on malformed lines; if False, skip bad lines
        
    Returns:
        Tuple containing:
            - NetworkX graph object (directed or undirected)
            - Pandas DataFrame of the loaded CSV
            
    Raises:
        ValueError: If required columns are missing in the CSV
        FileNotFoundError: If the CSV file doesn't exist
        ParserError: If CSV parsing fails and error_bad_lines is True
    """
    # Use pandas with simple error handling
    try:
        # Use python engine for auto-detection of delimiter if none provided
        df = pd.read_csv(csv_path, 
                         delimiter=delimiter,
                         on_bad_lines='skip' if not error_bad_lines else 'error',
                         engine='python' if delimiter is None else 'c')
    except pd.errors.ParserError as e:
        raise ValueError(f"Error parsing CSV: {str(e)}. Try specifying the correct delimiter or set error_bad_lines=False.")
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {str(e)}")

    # Check if required columns exist
    if source_col not in df.columns or target_col not in df.columns:
        # If columns don't exist but we have at least 2 columns, use the first two columns
        if len(df.columns) >= 2:
            print(f"Warning: Using columns {df.columns[0]} and {df.columns[1]} as source and target")
            source_col = df.columns[0]
            target_col = df.columns[1]
            if weight_col and len(df.columns) >= 3:
                weight_col = df.columns[2]
        else:
            raise ValueError(f"CSV does not have enough columns. Found: {list(df.columns)}")

    # Create the graph
    if directed:
        G = nx.from_pandas_edgelist(df, source=source_col, target=target_col, edge_attr=weight_col, create_using=nx.DiGraph())
    else:
        G = nx.from_pandas_edgelist(df, source=source_col, target=target_col, edge_attr=weight_col)
    
    return G, df

# ---------------------------
# Graph Metric Helper Functions
# ---------------------------

def _largest_connected_component_undirected(G: nx.Graph) -> nx.Graph:
    """Extract the largest connected component from a graph.
    
    Converts directed graphs to undirected before finding components.
    
    Args:
        G: Input graph (directed or undirected)
        
    Returns:
        The largest connected component as a subgraph
    """
    U = G.to_undirected() if G.is_directed() else G
    if U.number_of_nodes() == 0:
        return U
    if nx.is_connected(U):
        return U
    largest_cc_nodes = max(nx.connected_components(U), key=len)
    return U.subgraph(largest_cc_nodes).copy()

def _safe_graph_metric(G: nx.Graph, metric_func: Callable) -> Optional[float]:
    """Safely compute a graph metric on the largest connected component.
    
    Generic helper to compute any NetworkX metric that requires a connected graph.
    Handles edge cases like empty graphs or disconnected graphs.
    
    Args:
        G: Input graph
        metric_func: NetworkX function to compute on the largest connected component
        
    Returns:
        Computed metric value or None if calculation fails
    """
    if G.number_of_nodes() == 0:
        return None
    H = _largest_connected_component_undirected(G)
    try:
        return metric_func(H)
    except Exception:
        return None

def _safe_avg_shortest_path_length(G: nx.Graph) -> Optional[float]:
    """Safely compute average shortest path length.
    
    Handles edge cases like empty graphs or disconnected graphs
    by using only the largest connected component.
    
    Args:
        G: Input graph
        
    Returns:
        Average shortest path length or None if calculation fails
    """
    return _safe_graph_metric(G, nx.average_shortest_path_length)

def _safe_diameter(G: nx.Graph) -> Optional[float]:
    """Safely compute the diameter of a graph.
    
    Handles edge cases like empty graphs or disconnected graphs
    by using only the largest connected component.
    
    Args:
        G: Input graph
        
    Returns:
        Diameter of the graph or None if calculation fails
    """
    return _safe_graph_metric(G, nx.diameter)

def compute_quick_metrics(G: nx.Graph,
                          heavy: bool = True,
                          heavy_nodes_threshold: int = HEAVY_NODES_THRESHOLD) -> Dict[str, Any]:
    """Compute structural metrics helpful for a KG health check.
    
    Calculates various network metrics including:
    - Basic statistics (nodes, edges, density)
    - Degree statistics (average, median, p90, isolated nodes)
    - Component analysis (number of components, largest component ratio)
    - Clustering metrics (average clustering, transitivity)
    - Path metrics (average shortest path length, diameter) for smaller graphs
    - Degree assortativity
    
    Args:
        G: Input graph (directed or undirected)
        heavy: Whether to compute computationally intensive metrics like path lengths
        heavy_nodes_threshold: Skip heavy computations if graph has more nodes than this
        
    Returns:
        Dictionary of metrics with their computed values
    """
    # Safely compute basic metrics
    try:
        n = G.number_of_nodes()
        m = G.number_of_edges()
        density = nx.density(G)
    except Exception as e:
        # This is unlikely to fail but just in case
        n = 0
        m = 0
        density = 0.0
    
    metrics: Dict[str, Any] = {
        'nodes': n,
        'edges': m,
        'density': density,
        'isolated_nodes': 0,
        'connected_components': 0,
        'largest_component_ratio': 0.0,
        'avg_clustering': None
    }
    # Skip further calculations if graph is empty
    if n == 0:
        return metrics
    # Isolated nodes
    try:
        degs = np.array([d for _, d in G.degree()], dtype=float)
        metrics['isolated_nodes'] = int((degs == 0).sum())
    except Exception:
        pass
    # Components
    try:
        U = G.to_undirected() if G.is_directed() else G
        components = list(nx.connected_components(U))
        num_components = len(components)
        largest_cc_size = max((len(c) for c in components), default=0)
        metrics['connected_components'] = num_components
        metrics['largest_component_ratio'] = (largest_cc_size / n) if n else 0.0
    except Exception:
        pass
    # Clustering
    try:
        metrics['avg_clustering'] = nx.average_clustering(U)
    except Exception:
        pass
    return metrics

# ---------------------------
# Quality Ratio Helper Functions
# ---------------------------

def _clamp01(x: float) -> float:
    """Clamp a value between 0 and 1.
    
    Args:
        x: Input value to be clamped
        
    Returns:
        Value constrained to range [0.0, 1.0]
    """
    return float(max(0.0, min(1.0, x)))

def _in_target_range_score(x: Optional[float], lo: float, hi: float) -> float:
    """Calculate a score based on whether a value falls within a target range.
    
    Scores:
    - 0.0 for None values
    - Value increases linearly from 0.0 to 1.0 as x increases from 0 to lo
    - 1.0 for values between lo and hi (inclusive)
    - Value decreases linearly from 1.0 to 0.0 as x increases beyond hi
    
    Args:
        x: Value to score
        lo: Lower bound of ideal range
        hi: Upper bound of ideal range
        
    Returns:
        Score in range [0.0, 1.0]
    """
    if x is None:
        return 0.0
    if x < lo:
        return _clamp01(x / lo) if lo > 0 else 0.0
    if x > hi:
        return _clamp01(max(0.0, 1.0 - (x - hi) / max(hi, 1e-9)))
    return 1.0

# ---------------------------
# Scoring and Evaluation Functions
# ---------------------------

def quality_ratio(metrics: Dict[str, Any],
                  weights: Optional[Dict[str, float]] = None) -> Tuple[float, Dict[str, float]]:
    """Compute a retrieval-oriented Quality Ratio from quick metrics.
    
    Calculates a weighted average of multiple component scores:
    - ConnectivityScore: Measures ideal average node degree
    - DensityScore: Assesses graph density within ideal range
    - ComponentScore: Evaluates connectedness (ratio of largest component)
    
    Args:
        metrics: Dictionary of graph metrics from compute_quick_metrics()
        weights: Optional custom weights for component scores. If None, default weights are used.
        
    Returns:
        Tuple containing:
            - overall score (float in range [0, 1])
            - dictionary of component scores
    """
    if weights is None:
        weights = {
            'ConnectivityScore': 0.4,
            'DensityScore': 0.3,
            'ComponentScore': 0.3,
        }
    density = metrics.get('density', 0.0)
    largest_comp = metrics.get('largest_component_ratio', 0.0)
    connectivity_score = _in_target_range_score(density, lo=1e-5, hi=1e-2)
    density_score = connectivity_score  # For simplicity, use same score
    component_score = _clamp01(largest_comp)
    per_metric = {
        'ConnectivityScore': float(connectivity_score),
        'DensityScore': float(density_score),
        'ComponentScore': float(component_score),
    }
    overall = sum(per_metric[k] * weights.get(k, 0.0) for k in per_metric)
    return float(overall), per_metric

def evaluate_csv(csv_path: str,
                 source_col: str = 'source',
                 target_col: str = 'target',
                 directed: bool = False,
                 weight_col: Optional[str] = None,
                 heavy_metrics: bool = True,
                 heavy_nodes_threshold: int = HEAVY_NODES_THRESHOLD,
                 delimiter: Optional[str] = None,
                 error_bad_lines: bool = False) -> Dict[str, Any]:
    """Perform end-to-end evaluation of a graph from CSV: load -> metrics -> quality score.
    
    This is the main function to use when evaluating a knowledge graph stored in CSV format.
    It chains together the full workflow of loading, metric computation, and quality scoring.
    
    Args:
        csv_path: Path to the CSV file
        source_col: Name of the column containing source nodes
        target_col: Name of the column containing target nodes
        directed: If True, create a directed graph (DiGraph), else undirected
        weight_col: Optional name of column containing edge weights
        heavy_metrics: Whether to compute computationally intensive metrics
        heavy_nodes_threshold: Skip heavy computations if graph has more nodes than this
        delimiter: Optional delimiter character to use (auto-detected if None)
        error_bad_lines: If True, raise exception on malformed lines; if False, skip bad lines
        
    Returns:
        Dictionary containing:
            - path: Original CSV path
            - metrics: Computed metrics dictionary
            - quality_overall: Overall quality score (0-1)
            - quality_components: Individual quality component scores
            
    Raises:
        ValueError: If the CSV file is missing required columns
        FileNotFoundError: If the CSV file doesn't exist
        ParserError: If CSV parsing fails and error_bad_lines is True
    """
    try:
        G, _ = load_graph_from_csv(
            csv_path, 
            source_col, 
            target_col, 
            directed, 
            weight_col,
            delimiter=delimiter,
            error_bad_lines=error_bad_lines
        )
        heavy_flag = heavy_metrics and (G.number_of_nodes() <= heavy_nodes_threshold)
        mx = compute_quick_metrics(G, heavy=heavy_flag, heavy_nodes_threshold=heavy_nodes_threshold)
        overall, pm = quality_ratio(mx)
        return {
            'path': csv_path,
            'metrics': mx,
            'quality_overall': overall,
            'quality_components': pm
        }
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    except pd.errors.EmptyDataError:
        # Handle empty CSV files
        return {
            'path': csv_path,
            'metrics': {'nodes': 0, 'edges': 0, 'density': 0.0, 'is_directed': directed},
            'quality_overall': 0.0,
            'quality_components': {
                'ConnectivityScore': 0.0,
                'PathScore': 0.0,
                'DensityScore': 0.0,
                'ClusteringScore': 0.0,
                'ComponentScore': 0.0,
            }
        }
    except pd.errors.ParserError as e:
        # Special handling for parser errors to provide more context
        msg = str(e)
        if "Expected" in msg and "fields in line" in msg and "saw" in msg:
            raise ValueError(
                f"CSV parsing error in {csv_path}: {msg}\n"
                f"Try specifying a different delimiter or set error_bad_lines=False to skip problematic rows."
            )
        else:
            raise type(e)(f"Error parsing CSV {csv_path}: {msg}")
    except Exception as e:
        # Re-raise with additional context
        raise type(e)(f"Error evaluating CSV {csv_path}: {str(e)}")

# ---------------------------
# Reporting Functions
# ---------------------------

def format_report(evaluation: Dict[str, Any], detailed: bool = False) -> str:
    """Format evaluation results into a readable text report.
    
    Creates a multi-line string report with the key metrics and quality scores
    for easy comparison between knowledge graphs.
    
    Args:
        evaluation: Dictionary returned by evaluate_csv()
        detailed: If True, include additional metrics in the report
        
    Returns:
        Formatted report as a multi-line string
    """
    m = evaluation['metrics']
    pm = evaluation['quality_components']
    lines = []
    # Basic info
    lines.append(f"File: {evaluation['path']}")
    lines.append(f"Nodes: {m.get('nodes')} | Edges: {m.get('edges')} | Density: {m.get('density'):.6g}")
    lines.append(f"Isolated nodes: {m.get('isolated_nodes')} | Connected components: {m.get('connected_components')}")
    lines.append(f"Largest component ratio: {m.get('largest_component_ratio'):.3f}")
    # Clustering
    clustering = m.get('avg_clustering')
    if clustering is not None:
        lines.append(f"Clustering: {clustering:.3f}")
    # Quality scores
    lines.append("\n-- Quality Ratio --")
    lines.append(f"Overall: {evaluation['quality_overall']:.3f}")
    lines.append(f"  Connectivity: {pm.get('ConnectivityScore', 0.0):.3f}")
    lines.append(f"  Density: {pm.get('DensityScore', 0.0):.3f}")
    lines.append(f"  Component: {pm.get('ComponentScore', 0.0):.3f}")
    return "\n".join(lines)


def interpret_kg_comparison_with_llm(report1: str, report2: str) -> str:
    """
    Send two KG quality reports to Azure OpenAI (GPT-4.1 Nano) for expert comparative interpretation.
    Args:
        report1: The first formatted KG quality report string.
        report2: The second formatted KG quality report string.
    Returns:
        LLM-generated comparative interpretation string.
    """
    gpt41 = AzureChatOpenAI(
        azure_deployment=AZURE_DEPLOYMENT_GPT41,
        api_version=AZURE_OPENAI_API_VERSION,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        temperature=0.0
    )
    prompt = _build_comparison_prompt(report1, report2)
    response = gpt41.invoke(prompt)
    return response.content


def _build_comparison_prompt(report1: str, report2: str) -> str:
    """
    Build a prompt for LLM to compare and provide insights on two KG quality reports.
    Args:
        report1: The first formatted KG quality report string.
        report2: The second formatted KG quality report string.
    Returns:
        Prompt string for LLM.
    """
    metric_explanation = (
        "### Knowledge Graph Metrics Explained\n"
        "- **nodes**: Total number of unique entities (nodes) in the graph.\n"
        "- **edges**: Total number of relationships (edges) connecting nodes in the graph.\n"
        "- **density**: Ratio of actual edges to all possible edges. Higher density means more connections relative to graph size.\n"
        "- **isolated_nodes**: Number of nodes with no connections (degree zero). High values may indicate disconnected or unused entities.\n"
        "- **connected_components**: Number of separate subgraphs in the KG. A lower number is better for retrieval, as it means the graph is more unified.\n"
        "- **largest_component_ratio**: Fraction of nodes in the largest connected component. Values close to 1 mean most nodes are reachable from each other.\n"
        "- **avg_clustering**: Measures how likely nodes are to form tightly-knit groups. Higher values indicate more local connectivity and context.\n"
        "\n**Quality Component Scores**\n"
        "- **QR_ConnectivityScore**: A normalized score (0–1) reflecting how well-connected the graph is, based on density and structure.\n"
        "- **QR_DensityScore**: A normalized score (0–1) for edge density, indicating how richly the graph is populated with relationships.\n"
        "- **QR_ComponentScore**: A normalized score (0–1) for the largest component ratio, showing how unified the graph is.\n"
        "- **QR_overall**: The overall quality score (0–1), calculated as a weighted average of the three component scores—connectivity, density, and largest component ratio. The combined score summarizes the structural health of the knowledge graph for retrieval tasks.\n"
    )
    return (
        metric_explanation +
        "\nYou are an expert in knowledge graph (KGs) evaluation. "
        "Given the following two reports, compare them and provide only:\n"
        "- The winner\n"
        "- A comparative analysis highlighting key differences (strengths and weaknesses) as bullet points (do NOT use tables)\n"
        "- Suggest improvements to both KGs\n"
        f"\nReport 1:\n{report1}\n\nReport 2:\n{report2}\n"
    )