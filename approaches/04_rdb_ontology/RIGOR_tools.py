import json 
import re


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
        # Raw DDL
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
            'raw_ddl': raw_ddl,
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys
        }

    return result





def process_table(table_name, schema, llm, processed_tables, results):
    if table_name in processed_tables:
        return
    processed_tables.add(table_name)
    table = schema[table_name]

    # Generate delta ontology
    prompt = f"""
        Generate ontology elements with provenance annotations for database table {table_name} based on:

        [CONTEXT]
        - Database Schema of the table {json.dumps(table)}

        [INSTRUCTIONS]
        1. Include these elements:
            Classes (subclass of Thing)
            Data properties with domain/range
            Object properties with domain/range
            Use only one rdfs:domain and one rdfs:range per property. If multiple options exist, select the most general or create a shared superclass.
        3. Do not create a property named "is". Use rdf:type for instance membership, rdfs:subClassOf for class hierarchies, and owl:sameAs for instance equality.
        4. Use this format example:

        Class: {table_name}
        Annotations:
        prov:wasDerivedFrom
        <http://example.org/provenance/{table_name}>

        DataProperty:
        has_column_name
        domain {table_name}
        range string
        Annotations:
        prov:wasDerivedFrom
        <http://example.org/provenance/{table_name}/column_name>

        ObjectProperty:
        relates_to_table domain {table_name}
        range RelatedTable
        Annotations:
        prov:wasDerivedFrom
        <http://example.org/provenance/{table_name}/fk_column>

        Only output Manchester Syntax and nothing else. [OUTPUT]
    """
    delta_ontology = llm.invoke(prompt)

    # Revise delta ontology
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
       - Only one `rdfs:domain` and one `rdfs:range` per property.

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
       b. A corrected Manchester Syntax version of the ontology fragment.

    Do NOT include any other commentary outside this format.
    """
    revision = llm.invoke(evaluator_prompt)
    print(f"Table: {table_name}\nRevision:\n{revision}\n")

    results[table_name] = {
        "delta_ontology": delta_ontology,
        "revision": revision
    }

    # Recursively process referenced tables via foreign keys
    for fk in table['foreign_keys']:
        ref_table = fk['ref_table']
        if ref_table in schema:
            process_table(ref_table, schema, llm, processed_tables, results)




# --------------------------------------------------------------------------------------------------------------------------------------


def merge_ontologies(delta_ontology: str, core_ontology: str = "") -> str:
    """
    Merges a delta ontology into a growing core ontology.
    
    Args:
        delta_ontology: Manchester syntax ontology fragment to merge
        core_ontology: Existing core ontology (Manchester syntax)
        
    Returns:
        Merged ontology in Manchester syntax
    """
    
    # If core ontology is empty, start with basic structure
    if not core_ontology.strip():
        core_ontology = """Prefix: owl: <http://www.w3.org/2002/07/owl#>
    Prefix: rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    Prefix: rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    Prefix: prov: <http://www.w3.org/ns/prov#>
    Prefix: xsd: <http://www.w3.org/2001/XMLSchema#>

    Ontology: <http://example.org/merged-granter-ontology>

    """
    
    # Extract existing elements from core ontology
    existing_elements = extract_ontology_elements(core_ontology)
    
    # Extract new elements from delta ontology
    delta_elements = extract_ontology_elements(delta_ontology)
    
    # Merge elements (avoid duplicates)
    merged_elements = existing_elements.copy()
    
    for element_name, element_def in delta_elements.items():
        if element_name not in merged_elements:
            merged_elements[element_name] = element_def
        else:
            # Element exists, merge annotations if different
            merged_elements[element_name] = merge_element_definitions(
                merged_elements[element_name], element_def
            )
    
    # Reconstruct ontology
    return reconstruct_ontology(merged_elements, core_ontology)


def extract_ontology_elements(ontology_text: str) -> dict:
    """
    Extract ontology elements (classes, properties) from Manchester syntax text.
    
    Returns:
        Dictionary mapping element names to their full definitions
    """
    elements = {}
    
    # Split into blocks by empty lines or new element declarations
    blocks = re.split(r'\n(?=(?:Class:|DataProperty:|ObjectProperty:))', ontology_text)
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Extract element name
        if block.startswith('Class:'):
            name_match = re.search(r'Class:\s*(\S+)', block)
        elif block.startswith('DataProperty:'):
            name_match = re.search(r'DataProperty:\s*(\S+)', block)
        elif block.startswith('ObjectProperty:'):
            name_match = re.search(r'ObjectProperty:\s*(\S+)', block)
        else:
            continue
            
        if name_match:
            element_name = name_match.group(1)
            elements[element_name] = block
            
    return elements


def merge_element_definitions(existing_def: str, new_def: str) -> str:
    """
    Merge two element definitions, combining annotations.
    """
    # For simplicity, if elements have same name, keep existing and add new annotations
    lines_existing = existing_def.split('\n')
    lines_new = new_def.split('\n')
    
    # Find annotations in new definition that aren't in existing
    new_annotations = []
    in_annotations = False
    
    for line in lines_new:
        line = line.strip()
        if line == 'Annotations:':
            in_annotations = True
            continue
        elif line.startswith(('Class:', 'DataProperty:', 'ObjectProperty:', 'domain', 'range')):
            in_annotations = False
        elif in_annotations and line:
            # Check if this annotation exists in existing definition
            if line not in existing_def:
                new_annotations.append(line)
    
    # Add new annotations to existing definition
    if new_annotations:
        result_lines = lines_existing.copy()
        
        # Find where to insert annotations
        annotation_idx = None
        for i, line in enumerate(result_lines):
            if line.strip() == 'Annotations:':
                annotation_idx = i
                break
        
        if annotation_idx is not None:
            # Insert after existing annotations
            insert_idx = annotation_idx + 1
            while (insert_idx < len(result_lines) and 
                   result_lines[insert_idx].strip() and 
                   not result_lines[insert_idx].strip().startswith(('Class:', 'DataProperty:', 'ObjectProperty:'))):
                insert_idx += 1
            
            for ann in new_annotations:
                result_lines.insert(insert_idx, ann)
                insert_idx += 1
        else:
            # Add annotations section
            result_lines.append('Annotations:')
            result_lines.extend(new_annotations)
        
        return '\n'.join(result_lines)
    
    return existing_def


def reconstruct_ontology(elements: dict, base_ontology: str) -> str:
    """
    Reconstruct the complete ontology from elements.
    """
    # Extract prefixes and ontology declaration from base
    lines = base_ontology.split('\n')
    header_lines = []
    
    for line in lines:
        if (line.startswith('Prefix:') or 
            line.startswith('Ontology:') or 
            line.strip() == '' and len(header_lines) < 10):  # Keep initial empty lines
            header_lines.append(line)
        elif line.startswith(('Class:', 'DataProperty:', 'ObjectProperty:')):
            break
        elif not line.strip() and not header_lines:
            continue
        else:
            header_lines.append(line)
    
    # Group elements by type
    classes = []
    data_properties = []
    object_properties = []
    
    for element_def in elements.values():
        if element_def.startswith('Class:'):
            classes.append(element_def)
        elif element_def.startswith('DataProperty:'):
            data_properties.append(element_def)
        elif element_def.startswith('ObjectProperty:'):
            object_properties.append(element_def)
    
    # Reconstruct ontology
    result = []
    result.extend(header_lines)
    
    if classes:
        result.append('')
        result.append('# Classes')
        for cls in sorted(classes):
            result.append(cls)
            result.append('')
    
    if data_properties:
        result.append('# Data Properties')
        for prop in sorted(data_properties):
            result.append(prop)
            result.append('')
    
    if object_properties:
        result.append('# Object Properties')
        for prop in sorted(object_properties):
            result.append(prop)
            result.append('')
    
    return '\n'.join(result)

