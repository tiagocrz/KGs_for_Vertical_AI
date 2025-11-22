# KGs_for_Vertical_AI

## Project Overview
KGs_for_Vertical_AI is a toolkit for building, testing, and comparing Knowledge Graph (KG) and Retrieval-Augmented Generation (RAG) approaches for vertical AI applications. It provides scripts, notebooks, and utilities to extract ontologies from databases and text, construct knowledge graphs, and experiment with RAG techniques.


## Directory Structure

- **src/**: All main Python code, modules, and utilities for KG/RAG logic.
- **notebooks/**: Jupyter notebooks for experiments, demos, and workflow documentation, organized by approach.
- **data/**: Raw input data, with subfolders for PDFs, texts, and database.
- **results/**: Generated artifacts, including indexes (e.g., FAISS), KGs, and ontologies.
- **requirements.txt**, **README.md**: Root-level config and documentation.



## Main Components

### KG from Database
- `src/rdb_ontology_learning.py`: Extracts ontology from relational databases (Adapted RIGOR methodology).
- `src/build_kg.py`: Builds the knowledge graph from the extracted ontology.

### KG from Text
- `src/txt_ontology_learning.py`: Extracts ontology from text documents.
- `src/build_kg.py`: Builds the knowledge graph from the extracted ontology.

### RAG (Retrieval-Augmented Generation)
- Implemented in `src/rag/rag_tests.py` and uses code from `src/rag/rag_tools.py`.



## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Explore the notebooks in `notebooks/` for step-by-step guides and experiments.
3. Use scripts in `src/` to extract ontologies and build KGs.



## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new approaches.