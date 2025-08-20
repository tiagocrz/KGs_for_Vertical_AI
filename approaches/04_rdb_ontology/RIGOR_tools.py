import re
import json
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import os # remove from here

from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

llama32 = OllamaLLM(model="llama3.2:3b")
embedding = OllamaEmbeddings(model="nomic-embed-text:v1.5")

INDEX_PATH_CORE = "../../storage/faiss_RIGOR/core"
INDEX_PATH_EXTERNAL_ONT = "../../storage/faiss_RIGOR/external_ontologies"
INDEX_PATH_TEXTUAL_DESC = "../../storage/faiss_RIGOR/textual_descriptions"











def parse_mysql_ddl_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        ddl = f.read()

    # Remove comments and MySQL directives
    ddl = re.sub(r'/\*.*?\*/', '', ddl, flags=re.DOTALL)
    ddl = re.sub(r'--.*?$', '', ddl, flags=re.MULTILINE)
    ddl = re.sub(r'/\!.*?\*/;', '', ddl, flags=re.DOTALL)
    ddl = re.sub(r'/\!.*?\*/', '', ddl, flags=re.DOTALL)

    # Find all CREATE TABLE statements (handles backticks and multiline)
    table_regex = re.compile(
        r'CREATE TABLE\s+`?(\w+)`?\s*\((.*?)\)\s*ENGINE=.*?;',
        re.DOTALL | re.IGNORECASE
    )
    tables = table_regex.findall(ddl)
    result = {}

    for table_name, table_body in tables:
        # Raw DDL - not used anymore
        raw_ddl = f"CREATE TABLE `{table_name}` ({table_body});"

        # Split lines, remove empty and trailing commas
        lines = [line.strip().rstrip(',') for line in table_body.splitlines() if line.strip()]
        columns = []
        primary_keys = []
        foreign_keys = []

        for line in lines:
            # Column definition (starts with backtick or word, not constraint)
            if re.match(r'^`?\w+`?\s', line) and not line.upper().startswith(('PRIMARY KEY', 'FOREIGN KEY', 'CONSTRAINT', 'UNIQUE', 'KEY')):
                col_name = re.match(r'^`?(\w+)`?', line).group(1)
                columns.append(col_name)
            # Primary key
            elif line.upper().startswith('PRIMARY KEY'):
                pk_match = re.search(r'\((.*?)\)', line)
                if pk_match:
                    pk_cols = [col.strip(' `') for col in pk_match.group(1).split(',')]
                    primary_keys.extend(pk_cols)
            # Foreign key
            elif line.upper().startswith('CONSTRAINT') and 'FOREIGN KEY' in line.upper():
                fk_match = re.search(r'FOREIGN KEY\s*\((.*?)\)\s*REFERENCES\s*`?(\w+)`?\s*\((.*?)\)', line, re.IGNORECASE)
                if fk_match:
                    fk_cols = [col.strip(' `') for col in fk_match.group(1).split(',')]
                    ref_table = fk_match.group(2)
                    ref_cols = [col.strip(' `') for col in fk_match.group(3).split(',')]
                    foreign_keys.append({
                        'columns': fk_cols,
                        'ref_table': ref_table,
                        'ref_columns': ref_cols
                    })

        result[table_name] = {
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys
        }

    return result










def extract_ontology_lexical_view(ontology_path: str) -> list:
    """
    Returns format: ['label: comment', 'label2: comment2']
    Pairs labels with their corresponding comments in the DINGO ontology
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
    comments.pop(0) # Remove the first comment as it does not correspond to any label

    # Pair them sequentially (comment[i] goes with label[i])
    for i in range(len(labels)):
        if i < len(comments):
            lexical_view.append(f"{labels[i]}: {comments[i]}")
        else:
            lexical_view.append(f"{labels[i]}: ")
    
    return lexical_view










def chunk_text(text: str, chunk_size=1200, chunk_overlap=100):
    """
    Chunk text and return plain strings (no metadata)
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_text(text)










def embed_and_index(text_chunks: list, index_path: str):
    """
    Embed and index text chunks in the given directory
    """
    os.makedirs(os.path.dirname(index_path), exist_ok=True)

    vectorstore = FAISS.from_texts(text_chunks, embedding)
    vectorstore.save_local(index_path)
    print(f"Index saved at {index_path}. {len(text_chunks)} text chunks embedded and stored.")








def retrieve(input, index_path, k=4):
    vectorstore = FAISS.load_local(index_path, embedding, 
                                   allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(input, k=k)

    return [doc.page_content for doc in docs]







def docTable(relation: str):
    """
    returns the textual description of a relation r
    """
    return retrieve(f"relation: {relation}", INDEX_PATH_TEXTUAL_DESC, 2)


def docAttr(relation: str, attribute: str):
    """
    returns the textual description of an attribute a in relation r
    """
    return retrieve(f"relation: {relation}, attribute: {attribute}", INDEX_PATH_TEXTUAL_DESC, 1)























schema = parse_mysql_ddl_file('../../database/schema/usable_schema.sql')