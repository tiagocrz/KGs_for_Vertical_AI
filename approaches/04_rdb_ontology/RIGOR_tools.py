import re
import json
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import os # remove from here

from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

llama32 = OllamaLLM(model="llama3.2:3b")
embedding = OllamaEmbeddings(model="nomic-embed-text:v1.5")



from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq

groqllm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=GROQ_API_KEY,
    temperature=0
)


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
















def extract_ontology_block(text: str) -> str:
    """
    Extracts the ontology code block (Manchester Syntax) from a mixed LLM output.
    Looks for content between triple backticks (```).

    Parameters:
        text (str): The full output from the LLM.

    Returns:
        str: The extracted ontology block as a string, or an empty string if not found.
    """
    inside_block = False
    lines = []
    
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if inside_block:
                break  # end of block
            else:
                inside_block = True
                continue  # skip the line with ```
        if inside_block:
            lines.append(line)
    
    return "\n".join(lines).strip()







def build_table_ontology(table_name: str, table_schema: dict, core_ontology: str):
    prompt = f"""
    Generate ontology elements with provenance annotations for database table {table_name} based on:

    [CONTEXT]
    - Database Schema of the table \n{json.dumps(table_schema)}\n
    - Take semantics from the External Ontology Knowledge \n{"\n".join(retrieve(table_name, INDEX_PATH_EXTERNAL_ONT))}\n
    - Take semantics from the Relevant Documents \n{"\n".join(docTable(table_name))}

    [INSTRUCTIONS]
    1. Include these elements:
        Classes (subclass of Thing)
        Data properties with domain/range
        Object properties with domain/range
        Use only one Domain: and one Range: per property. If multiple options exist, select the most general or create a shared superclass.
    3. Do not create a property named "is". Use rdf:type for instance membership, rdfs:subClassOf for class hierarchies, and owl:sameAs for instance equality.
    4. Use this format example:

    Prefix: prov: <http://www.w3.org/ns/prov#>
    Prefix: xsd: <http://www.w3.org/2001/XMLSchema#>
    Ontology: <http://example.org/my-ontology>

    Class: {table_name}
    Annotations:
        prov:wasDerivedFrom <http://example.org/provenance/{table_name}>

    DataProperty: has_column_name
    Domain: {table_name}
    Range: xsd:string
    Annotations:
        prov:wasDerivedFrom <http://example.org/provenance/{table_name}/column_name>

    ObjectProperty: relates_to_table
    Domain: {table_name}
    Range: RelatedTable
    Annotations:
        prov:wasDerivedFrom <http://example.org/provenance/{table_name}/fk_column>


    Only output Manchester Syntax and nothing else. [OUTPUT]
    """

    delta_ontology = groqllm.invoke(prompt).content


    evaluator_prompt = f"""
    You are an expert in OWL 2 DL ontology modeling and validation.

    Your task is to review the following delta ontology fragment generated from a relational database table, along with its schema and relevant context.

    [DELTA-ONTOLOGY]
    {delta_ontology}

    [DATABASE SCHEMA]
    {table}

    [CORE ONTOLOGY CONTEXT]
    (empty as of now)

    [VALIDATION CRITERIA]
    1. **Coherence with Core Ontology**  
    - Do NOT redefine an existing class, property, or concept already present in the core ontology with the same meaning.
    - Reuse existing ontology elements where possible instead of creating duplicates.

    2. **Alignment with Input Table Schema**  
    - Every significant column and foreign key in the table must be represented as an appropriate ontology element (class, data property, or object property).
    - Naming should reflect the database semantics clearly and consistently.

    3. **Syntactic Validity**  
    - The ontology must conform to the OWL 2 DL profile and valid Manchester Syntax.

        [OWL 2 Manchester Syntax Validation Rules]

        Use **only** Manchester Syntax keywords: Class:, ObjectProperty:, DataProperty:, SubClassOf:, Annotations:, Domain:, Range:, Prefix:, Ontology:.

        DO NOT use:
        - RDF-style triples like `rdfs:subClassOf`, `a`, or `owl:Class`
        - Semicolons (;) or commas (,) inside blocks
        - Periods (.) at the end of annotation lines


        DO:
        - Use `SubClassOf:` **inside the Class: block** (not as `rdfs:subClassOf`)
        - Place `Annotations:` after `SubClassOf:` inside the same block
        - Use **line breaks only** to separate multiple annotations — no commas or semicolons
        - Enclose all IRIs (including annotation values and external links) in angle brackets: `<...>`
        - Declare every used prefix with `Prefix: ...` and include an `Ontology:` declaration
        - For each Property, define **exactly one** Domain: and one Range:
        - Ensure that all referenced classes or properties are explicitly declared in the ontology
        - Avoid duplicate declarations unless you're adding `SubClassOf:` or `Annotations:` to an existing element

        [Example Structure]

        Class: MyClass
            SubClassOf: ParentClass
            Annotations:
                prov:wasDerivedFrom <http://example.org/provenance/MyClass>

        DataProperty: has_value
            Domain: MyClass
            Range: xsd:string
            Annotations:
                prov:wasDerivedFrom <http://example.org/provenance/MyClass/has_value>

    4. **Logical Consistency**  
    - No contradictory class axioms or property constraints.
    - No circular subclass relationships.
    - Correct choice between object properties and data properties.

    5. **Clarity and Naming Quality**  
    - Use self-explanatory, domain-relevant names.
    - Avoid generic or meaningless labels (e.g., "Entity1", "PropertyA").
    - All properties should follow consistent naming patterns (e.g., `has_`, `is_...Of`).

    [YOUR TASK]
    - Check the delta ontology fragment against all criteria above.
    - If issues are found, provide a corrected version of the ontology in valid Manchester Syntax.
    - Make minimal necessary changes to preserve the author's intent while ensuring correctness and OWL 2 DL compliance.
    - Ensure all elements keep their provenance annotations.
    
    [OUTPUT FORMAT]
    Respond ONLY with:
    1. "Status: PASS" if the ontology fragment meets all criteria, or "Status: FAIL" if it does not.
    2. If FAIL, provide:
    a. A short bullet list of the issues found.
    b. A corrected Manchester Syntax version of the ontology fragment, and enclose it between triple backticks (```), on their own lines.

    Do NOT include any other commentary outside this format.
    Always enclose the corrected ontology with triple backticks for programmatic extraction.
    """

    revision = groqllm.invoke(evaluator_prompt).content

    
    if "Status: PASS" in revision:
        return delta_ontology
    else:
    # Extract corrected ontology from revision
       return extract_ontology_block(revision)