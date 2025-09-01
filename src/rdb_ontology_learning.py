import re
import json
from langchain_community.vectorstores import FAISS
#from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rdflib import Graph, RDF, OWL

from langchain_ollama import OllamaEmbeddings
embedding = OllamaEmbeddings(model="nomic-embed-text:v1.5")


from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
gpt41_nano = AzureChatOpenAI(
    azure_deployment=os.getenv("AZURE_DEPLOYMENT_GPT41_NANO"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    temperature=0.0
)


INDEX_PATH_CORE = "storage/faiss_RIGOR/core"
INDEX_PATH_EXTERNAL_ONT = "storage/faiss_RIGOR/external_ontologies"
INDEX_PATH_TEXTUAL_DESC = "storage/faiss_RIGOR/textual_descriptions"


# ---------------------------------- TOOLS ----------------------------------


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




def extract_names(turtle_str):
    """
    Extract ontology elements (local names without full URIs).
    Returns:
        - class_names: ontology classes (entities)
        - object_property_names: ontology object properties (relationships)
        - datatype_property_names: ontology datatype properties (attributes)
    """
    g = Graph()
    g.parse(data=turtle_str, format="turtle")
    
    def get_local_name(uri):
        uri_str = str(uri)
        if '#' in uri_str: 
            return uri_str.split('#')[-1]
        return uri_str.split('/')[-1]
    
    # Classes
    class_uris = [s for s, _, _ in g.triples((None, RDF.type, OWL.Class))]
    class_names = [get_local_name(uri) for uri in class_uris]
    
    # Object properties
    object_prop_uris = [s for s, _, _ in g.triples((None, RDF.type, OWL.ObjectProperty))]
    object_property_names = [get_local_name(uri) for uri in object_prop_uris]
    
    # Datatype properties
    data_prop_uris = [s for s, _, _ in g.triples((None, RDF.type, OWL.DatatypeProperty))]
    datatype_property_names = [get_local_name(uri) for uri in data_prop_uris]
    
    return (
        sorted(class_names),
        sorted(object_property_names),
        sorted(datatype_property_names),
    )




def extract_ontology_block(text: str) -> str:
    """
    Extracts the ontology code block from a mixed LLM output.
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




def validate_turtle_string(turtle_str: str) -> tuple[bool, str]:
    """
    Validates whether the input string is valid Turtle syntax.

    Returns:
        - is_valid (bool): True if valid, False otherwise
        - error_msg (str): Error message if invalid, else empty
    """
    try:
        g = Graph()
        g.parse(data=turtle_str, format="turtle")
        return True, ""
    except Exception as e:
        return False, str(e)




def build_table_ontology(table_name: str, table_schema: dict, core_ontology: str):

    classes, relations, attributes = extract_names(core_ontology)
    core_context = f"""Class names: {', '.join(classes)}
\nObject properties (relations): {', '.join(relations)}
\nDatatype properties (attributes): {', '.join(attributes)}
"""

    prompt = f"""
Generate ontology elements with provenance annotations for database table {table_name}, based on:

[CONTEXT]
- Database Schema of the table \n{json.dumps(table_schema)}\n
- Take semantics from the External Ontology Knowledge \n{"\n".join(retrieve(table_name, INDEX_PATH_EXTERNAL_ONT))}\n
- Take semantics from the Relevant Documents \n{"\n".join(docTable(table_name))}
- Take semantics from the Core Ontology Knowledge \n{core_context if core_ontology else "(empty as of now)"}\n

[INSTRUCTIONS]
1. Include these elements:
    Classes (subclass of owl:Thing)
    Data properties with domain/range
    Object properties with domain/range
    Use only one Domain:, one Range:, one Comment: and one Label: per property. If multiple options exist, select the most general or create a shared superclass.
2. Use Turtle/RDF syntax format
3. Do not create a property named "is". Use rdf:type for instance membership, rdfs:subClassOf for class hierarchies, and owl:sameAs for instance equality.
4. STRICT NAMING RULES:
   - Use PascalCase for ALL class names (e.g., Person, DatabaseTable, ProvenanceInfo)
   - Use camelCase for ALL property names (e.g., hasName, relatesTo, wasDerivedFrom)
   - NEVER use lowercase for class names
5. For each class and property, also generate an rdfs:label and an rdfs:comment that provides a concise human-readable description of its meaning and intended use.
6. Do not create duplicate elements. If one already exists in the Core Ontology Knowledge, reuse/revise it instead of creating a new one.
7. Use this format example:

@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://example.org/my-ontology#> .

:{table_name} a owl:Class ;
    prov:wasDerivedFrom <http://example.org/provenance/{table_name}> .

:has_column_name a owl:DatatypeProperty ;
    rdfs:domain :{table_name} ;
    rdfs:range xsd:string ;
    prov:wasDerivedFrom <http://example.org/provenance/{table_name}/column_name> .

:relates_to_table a owl:ObjectProperty ;
    rdfs:domain :{table_name} ;
    rdfs:range :RelatedTable ;
    prov:wasDerivedFrom <http://example.org/provenance/{table_name}/fk_column> .

Only output Turtle syntax and nothing else. [OUTPUT]
    """

    delta_ontology = gpt41_nano.invoke(prompt).content

    is_valid, error_message = validate_turtle_string(delta_ontology)

    if not is_valid:
        additional_syntax_hint = f"""
    [SYNTAX ISSUES DETECTED]

    Note: The delta ontology provided is NOT valid Turtle syntax.

    Please make the following minimal syntax corrections before further validation:
    - Declare all prefixes used in the ontology explicitly (e.g., rdf:, rdfs:, owl:, xsd:, prov:).
    - Use angle brackets <...> for all full IRI references.
    - Each property must have exactly one rdfs:domain and one rdfs:range.
    - Ensure rdfs:range only uses valid OWL classes or XSD types (e.g., xsd:string).
    - Remove annotation-style keywords like 'Annotations:' and instead use Turtle triples for metadata.
    - Avoid misplaced punctuation or unclosed blocks.

    Parsing error: {error_message}
    """
    else:
        additional_syntax_hint = ""


    evaluator_prompt = f"""
You are an expert in OWL 2 DL ontology modeling and validation.

Your task is to review the following delta ontology fragment generated from a relational database table, along with its schema and relevant context.

[DELTA-ONTOLOGY]
{delta_ontology}

[DATABASE SCHEMA]
{json.dumps(table_schema)}

[CORE ONTOLOGY CONTEXT]
{core_context if core_ontology else "(empty as of now)"}

{additional_syntax_hint}

[VALIDATION CRITERIA]
1. **Coherence with Core Ontology**  
- Do NOT redefine an existing class, property, or concept already present in the core ontology with the same meaning.
- Reuse existing ontology elements where possible instead of creating duplicates.

2. **Alignment with Input Table Schema**  
- Every significant column and foreign key in the table must be represented as an appropriate ontology element (class, data property, or object property).
- Naming should reflect the database semantics clearly and consistently.

3. **Syntactic Validity**  
- The ontology must conform to valid Turtle/RDF syntax.
- Use proper prefixes and IRI declarations.
- Exactly one rdfs:domain and one rdfs:range per property.

4. **Logical Consistency**  
- No contradictory class axioms or property constraints.
- No circular subclass relationships.
- Correct choice between object properties and data properties.

5. **Clarity and Naming Quality**  
- Use self-explanatory, domain-relevant names.
- Avoid generic or meaningless labels.
- All elements should follow camel case naming patterns.

[YOUR TASK]
- Check the delta ontology fragment against all criteria above.
- If issues are found, provide a corrected version of the ontology in valid Turtle syntax.
- Make minimal necessary changes to preserve the author's intent while ensuring correctness and OWL 2 DL compliance.
- Ensure all elements keep their provenance annotations.

[OUTPUT FORMAT]
Respond ONLY with:
1. "Status: PASS" if the ontology fragment meets all criteria, or "Status: FAIL" if it does not.
2. If FAIL, provide:
    a. A short bullet list of the issues found.
    b. A corrected Turtle syntax version of the ontology fragment, and enclose it between triple backticks (```), on their own lines.

Do NOT include any other commentary outside this format.
Always enclose the corrected ontology with triple backticks for programmatic extraction.
    """

    revision = gpt41_nano.invoke(evaluator_prompt).content

    if "Status: PASS" in revision:
        print("JudgeLLM Validation succeeded.")
        valid = validate_turtle_string(delta_ontology)
        print(valid)
        if valid[0]:
            return delta_ontology
        else:
            print("Syntax Validation failed.\n\n")
            return delta_ontology
    else:
        print("JudgeLLM Validation failed. Corrected Version:")
        valid = validate_turtle_string(extract_ontology_block(revision))
        print(valid)
        if valid[0]:
            return extract_ontology_block(revision)
        else:
            print("Syntax Validation failed.\n\n")
            return extract_ontology_block(revision)




def merge_ontologies_ttl(core_ttl: str, delta_ttl: str) -> str:
    """
    Merge two OWL ontologies in Turtle format (as strings) and return the merged ontology as a Turtle string.
    Uses RDFLib's built-in graph merging with automatic triple deduplication.
    
    Parameters:
        core_ttl (str): Core ontology (Turtle format string)
        delta_ttl (str): Delta ontology (Turtle format string)
        
    Returns:
        str: Merged ontology in Turtle syntax
    """
    # Parse both ontologies
    core_graph = Graph()
    core_graph.parse(data=core_ttl, format="turtle")

    delta_graph = Graph()
    delta_graph.parse(data=delta_ttl, format="turtle")

    # Merge delta into core
    core_graph += delta_graph  # RDFLib automatically deduplicates identical triples

    # Serialize the merged ontology back to Turtle
    return core_graph.serialize(format="turtle")




def sort_fk_chain(fk_tables, schema):
    """
    Sort tables by foreign key dependencies - referenced tables come first
    """
    ordered = []
    remaining = fk_tables.copy()
    
    while remaining:
        # Find tables whose FK references are already processed
        ready = []
        for table in remaining:
            fk_refs = [fk['ref_table'] for fk in schema[table]['foreign_keys']]
            # Check if all FK references are either already processed or have no FKs themselves
            if all(ref in ordered or ref not in fk_tables for ref in fk_refs):
                ready.append(table)
        
        if ready:
            ordered.extend(ready)
            for table in ready:
                remaining.remove(table)
        else:
            # Handle circular dependencies - just add remaining tables
            ordered.extend(remaining)
            break
    
    return ordered




def save_and_validate_ttl(ontology_string: str, filename: str = None):
    """
    Save ontology string as .ttl file with validation
    """
    # Validate first
    is_valid, error = validate_turtle_string(ontology_string)
    if not is_valid:
        print(f"Invalid Turtle syntax: {error}")
        return None
    
    output_dir = "output/ontologies/RDB"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    try:
        g = Graph()
        g.parse(data=ontology_string, format="turtle")
        g.serialize(destination=filepath, format="turtle")
        
        print(f"Ontology saved: {filename}")
        print(f"{len(g)} triples")
        print(f"{os.path.getsize(filepath):,} bytes")
        return filepath
    except Exception as e:
        print(f"Save failed: {e}")
        return None




# ---------------------------------- RUNNING ----------------------------------

if __name__ == "__main__":
    # Data structures
    schema = parse_mysql_ddl_file('database/schema/usable_schema.sql')

    with open('database/README.md', 'r', encoding='utf-8') as f:
        readme_database_content = f.read()
    readme_database_chunks = chunk_text(readme_database_content, 500)

    lexE = extract_ontology_lexical_view('approaches/04_rdb_ontology/external_ontologies/DINGO-Manchester.omn')

    index_list = [INDEX_PATH_EXTERNAL_ONT, INDEX_PATH_TEXTUAL_DESC]
    content_list = [lexE, readme_database_chunks]

    for i, content in enumerate(content_list):
        if not os.path.exists(index_list[i]) or not os.listdir(index_list[i]):
            embed_and_index(content, index_list[i])
            print(f"Indexed {len(content)} text chunks in {index_list[i]}.")

    # Processing order CHANGE
    table_names = list(schema.keys())
    no_fk_tables = [name for name in table_names if not schema[name]['foreign_keys']]
    fk_tables = [name for name in table_names if schema[name]['foreign_keys']]
    fk_tables = sort_fk_chain(fk_tables, schema)
    processing_order = no_fk_tables + fk_tables

    print(f"Processing {len(processing_order)} tables: {processing_order}")

    core_ontology = ""
    successful = []
    failed = []

    # Iterating over database tables
    for table in processing_order:
        print(f"Processing {table}...", end=" ")
        
        try:
            delta = build_table_ontology(table, schema[table], core_ontology)
            core_ontology = merge_ontologies_ttl(core_ontology, delta)
            print("✅")
            successful.append(table)
        except Exception as e:
            print(f"❌ {e}")
            failed.append(table)

    print(f"\nSuccess: {len(successful)}, Failed: {len(failed)}")
    if failed:
        print(f"Failed tables: {failed}")

    is_valid, error = validate_turtle_string(core_ontology)
    print(f"Final ontology valid: {is_valid}")
    if not is_valid:
        print(f"Error: {error}")

    # Retry failed tables
    if failed:
        print(f"\nRetrying {len(failed)} failed tables...")
        
        retry_successful = []
        retry_failed = []
        
        for table in failed:
            print(f"Retrying {table}...", end=" ")
            
            try:
                delta = build_table_ontology(table, schema[table], core_ontology)
                core_ontology = merge_ontologies_ttl(core_ontology, delta)
                print("✅")
                retry_successful.append(table)
            except Exception as e:
                print(f"❌ {e}")
                retry_failed.append(table)
        
        successful.extend(retry_successful)
        failed = retry_failed
        
        print(f"\nRetry Results:")
        print(f"Newly successful: {len(retry_successful)}")
        print(f"Still failed: {len(retry_failed)}")
    
    #print(core_ontology)
    # Save Ontology
    save_and_validate_ttl(core_ontology, 'rigor_ontology_few_fixes.ttl')