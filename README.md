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
- `src/rdb_ontology_learning.py`: Extracts ontology from relational databases (RIGOR methodology).
- `src/build_kg.py`: Builds the knowledge graph from the extracted ontology.

### KG from Text
- `src/txt_ontology_learning.py`: Extracts ontology from text documents. (Note: Issues with Portuguese language support.)
- `src/build_kg.py`: Builds the knowledge graph from the extracted ontology.

### RAG (Retrieval-Augmented Generation)
- Implemented in notebooks under `notebooks/01_vector_rag/` and uses code from `src/`.



## Getting Started
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Explore the notebooks in `notebooks/` for step-by-step guides and experiments.
3. Use scripts in `src/` to extract ontologies and build KGs.


## Usage
- To extract ontology from a database:
  ```bash
  python src/rdb_ontology_learning.py
  python src/build_kg.py
  ```
- To extract ontology from text:
  ```bash
  python src/txt_ontology_learning.py
  python src/build_kg.py
  ```
- For RAG experiments, see notebooks in `notebooks/01_vector_rag/`.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new approaches.

## License
Specify your license here (e.g., MIT, Apache 2.0).
