# KGs_for_Vertical_AI

## Project Overview
KGs_for_Vertical_AI is a toolkit for building, testing, and comparing Knowledge Graph (KG) and Retrieval-Augmented Generation (RAG) approaches for vertical AI applications. It provides scripts, notebooks, and utilities to extract ontologies from databases and text, construct knowledge graphs, and experiment with RAG techniques.

## Directory Structure

- **approaches/**: Notebooks with structured sequences for different KG and RAG approaches, including vector-based RAG.
- **comparison/**: Contains questions and scripts to compare the performance and results of different approaches.
- **data/**: Source documents (PDFs, texts) used for KG and RAG extraction.
- **database/**: Database schema and documentation for DB-based ontology extraction.
- **output/**: Generated ontologies and knowledge graphs.
- **src/**: Main source code for ontology extraction and KG construction.
- **storage/**: Indexes for RAG experiments (e.g., FAISS indexes).
- **tests/**: Scripts and notebooks for testing and experimentation.
- **utilitites/**: Helper functions and generic utilities (e.g., PDF to text conversion).

## Main Components

### KG from Database
- `rdb_ontology_learning.py`: Extracts ontology from relational databases (RIGOR methodology).
- `build_kg.py`: Builds the knowledge graph from the extracted ontology.

### KG from Text
- `txt_ontology_learning.py`: Extracts ontology from text documents. (Note: Issues with Portuguese language support.)
- `build_kg.py`: Builds the knowledge graph from the extracted ontology.

### RAG (Retrieval-Augmented Generation)
- Implemented inside `approaches/01_vector_rag/`.

## Getting Started
1. Install dependencies:
	 ```bash
	 pip install -r requirements.txt
	 ```
2. Explore the notebooks in `approaches/` for step-by-step guides.
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
- For RAG experiments, see `approaches/01_vector_rag/`.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new approaches.

## License
Specify your license here (e.g., MIT, Apache 2.0).
