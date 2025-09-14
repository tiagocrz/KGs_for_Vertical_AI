import nltk
from nltk import sent_tokenize
from typing import List
from rdflib import Graph

from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

gpt41_nano = AzureChatOpenAI(
    azure_deployment = os.getenv("AZURE_DEPLOYMENT_GPT41_NANO"),
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),
    temperature = 0.3
)

prompt_c_step_1 = "Extract classes in ttl format from the following text, only return the created ttl code. Make sure to label all classes as of type rdfs:Class: \n\n"

prompt_c_step_2 = """Extract individuals and relations in ttl format from the following sentence, based on the given classes.
Only return the ttl code, include the classes, individuals, and relations in this sentence. 
Make sure to label all classes as of rdfs:Class, all individuals as owl:NamedIndividual, and all properties as owl:ObjectProperty, owl:DatatypeProperty, or owl:AnnotationProperty. 

Follow correct Turtle syntax:
- Use ';' to separate multiple predicates for the same subject.
- Use ',' to separate multiple objects of the same predicate.
- End each subject block with '.' before starting a new subject.
- Do not switch subjects inside the same ';' chain.
"""

# ---------------------------------- TOOLS ----------------------------------

nltk.download('punkt')
def read_text_file(file: str) -> list:
    """
    Read a text file and return a list of sentences.
    """
    with open(file, 'r', encoding='utf-8') as file:
        text = file.read()
        sentences = nltk.sent_tokenize(text, language='portuguese')
    return sentences




def get_azure_response(text, prompt, ontology_info=None):
    """Get response from Azure OpenAI"""
    if ontology_info is None:
        message_content = f"{prompt}{text}"
    else:
        # Convert ontology_info list to string if needed
        if isinstance(ontology_info, list):
            ontology_info = "\n".join(ontology_info)
        message_content = f"{prompt} {text}, {ontology_info}"

    response = gpt41_nano.invoke([message_content])
    
    return response.content




def get_results_from_response(response_content: str) -> List[str]:
    """Extract results from Azure OpenAI response content"""
    standard_prefixes = [
        "@prefix : <http://example.org#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix prov: <http://www.w3.org/ns/prov#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
    ]
    try:
        response_content = response_content.split('\n')
        response_content = [line for line in response_content if not any(line.strip().startswith(prefix) 
                                                                         for prefix in standard_prefixes)]
        
        while '' in response_content: 
            response_content.remove('')
        while '```ttl' in response_content:
            response_content.remove('```ttl')
        while '```' in response_content:
            response_content.remove('```')
        return response_content
    except Exception as e:
        print(f'Error processing response: {e}')
        return []
    


#def clean_relations(relations: List):
#    ttl_output = []
#    for relation in relations:
#        for triple in relation:
#            if triple:
#                cleaned_triple = triple.strip().strip('```').strip("ttl").strip("```")
#                ttl_output.append(cleaned_triple)
#    return ttl_output
#
#
#                
#
#def gpt_results_to_ttl(relations: List):
#    ttl_output = "\n".join(clean_relations(relations))
#    return ttl_output




def gpt_results_to_ttl(relations: List, output: str):
    ttl_output = []
    clean_relations(relations, ttl_output)

    with open(output, 'w', encoding='utf-8') as f:
        f.write("\n".join(ttl_output))
        
    return "\n".join(ttl_output)


def clean_relations(relations, ttl_output):
    for relation in relations:
        for triple in relation:
            if triple:
                cleaned_triple = triple.strip().strip('```').strip("ttl").strip("```")
                ttl_output.append(cleaned_triple)




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




def build_validation_prompt(results, error_message) -> str:
        
    prompt_validator = f"""
    You are an expert in turtle ontology modeling and validation.
    Your task is to review the following generated ontology, and correct the syntax issues present.

    [ONTOLOGY INFO]
    {results}

    [SYNTAX ISSUES DETECTED]

    Note: The delta ontology provided is NOT valid Turtle syntax.

    Please make the following minimal syntax corrections before further validation:
    - Use angle brackets <...> for all full IRI references.
    - Each property must have exactly one rdfs:domain and one rdfs:range.
    - Ensure rdfs:range only uses valid OWL classes or XSD types (e.g., xsd:string).
    - Remove annotation-style keywords like 'Annotations:' and instead use Turtle triples for metadata.
    - Avoid misplaced punctuation or unclosed blocks.

    Parsing error: {error_message}

    [VALIDATION CRITERIA]
    **Syntactic Validity**  
    - The ontology must conform to valid Turtle/RDF syntax.
    - Use proper prefixes and IRI declarations.
    - Exactly one rdfs:domain and one rdfs:range per property.

    [YOUR TASK]
    - Check the ontology against the criteria above.
    - If issues are found, provide a corrected version of the given ontology in valid Turtle syntax.
    - Make minimal necessary changes to preserve the author's intent while ensuring correctness and turtle compliance.
    - The generated ontology does not have any declared prefixes purposely, so do NOT add any.

    [OUTPUT FORMAT]
    Respond ONLY with a corrected Turtle syntax version of the exact same ontology.
    Do NOT include any other commentary outside this format.
    Do NOT reduce the ontology content. Make only syntax adjustments.
    """
    return prompt_validator




def extract_ontology_block(text: str) -> str:
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




def save_and_validate_ttl(ontology_string: str, filename: str = None):
    """
    Save ontology string as .ttl file with validation
    """
    is_valid, error = validate_turtle_string(ontology_string)
    if not is_valid:
        print(f"Invalid Turtle syntax: {error}")
        return None
    
    output_dir = "results/ontologies/text"
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




def query_azure_gpt(text: list):
    """Query Azure GPT with the text"""
    relations = []

    try:
        response_1 = get_azure_response(text, prompt_c_step_1)
        
        for sentence in text:
            response_2 = get_azure_response(sentence, prompt_c_step_2, get_results_from_response(response_1))
            relations.append(get_results_from_response(response_2))

    except Exception as e:
        print(f"Error querying Azure GPT: {e}")
        return []

    print(f"Extracted {len(relations)} relation sets")
    return relations


# ---------------------------------- RUNNING ----------------------------------

if __name__ == "__main__":
    text = read_text_file('data/texts/application_example.txt')

    # Classes
    response_1 = get_azure_response(text, prompt_c_step_1)
    print(response_1)

    standard_prefixes = [
            "@prefix : <http://example.org#> .",
            "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
            "@prefix prov: <http://www.w3.org/ns/prov#> .",
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
            "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> ."
        ]

    # Relations and Individuals
    unsuccessful = []
    relations = []
    for i, sentence in enumerate(text):
        print(f"Processing sentence {i+1}/{len(text)}")
        response_2 = get_azure_response(sentence, prompt_c_step_2, 
                                        get_results_from_response(response_1))
        response_2_with_prefixes = ("\n".join(standard_prefixes) + 
                                    "\n" + 
                                    "\n".join(get_results_from_response(response_2)))

        is_valid, error_message = validate_turtle_string(response_2_with_prefixes)
        print(is_valid)

        retry_count = 0
        max_retries = 3
        while is_valid == False and retry_count < max_retries:
            print(f"Retrying attempt {retry_count+1}/{max_retries} to response {i+1} due to error: {error_message}")

            fix = gpt41_nano.invoke(build_validation_prompt(response_2_with_prefixes,  
                                                        error_message)).content
            retry_count += 1
            is_valid, error_message = validate_turtle_string(fix)

        if is_valid:
            print(f"Successfully validated response {i+1} after {retry_count} attempts.")
            relations.append(get_results_from_response(response_2))
        else:
            print(f"Failed to correct response {i+1} after {retry_count} attempts. Skipping.")
            unsuccessful.append((i, sentence))
            continue
        
    print(f"Successfully processed {len(text) - len(unsuccessful)} sentences.\n\nUnsuccessful sentences: {[text[i] for i, _ in unsuccessful]}")

    ontology = gpt_results_to_ttl(relations, 'results/ontologies/text/text_ontology_val.txt')

    #with open('results/ontologies/text/text_ontology_val.txt', 'r', encoding='utf-8') as f:
    #    ontology = f.read()

    # Add prefixes since gpt_results_to_ttl doesn't include them
    ontology = "\n".join(standard_prefixes) + "\n\n" + ontology
    print(ontology)

    is_valid, error_message = validate_turtle_string(ontology)
    filename = "text_ontology_val.ttl"

    if is_valid:
        print("Final ontology is valid Turtle syntax.")
        save_and_validate_ttl(ontology, filename=filename)

    else:
        print(f"Ontology is invalid: {error_message}")
        #current_ontology = ontology
        #for i in range(6):
        #    print(f"Attempt {i+1} to validate ontology")
        #    # validator_prompt = build_validation_prompt(current_ontology) 
        #    
        #    validator_prompt = build_merge_validation_prompt(relations)

        #    revision = gpt41_nano.invoke(validator_prompt).content
        #    current_ontology = extract_ontology_block(revision)
        #    print(current_ontology)
        #    is_valid, error_message = validate_turtle_string(current_ontology)
        #
        #    if is_valid:
        #        print("Final ontology is valid Turtle syntax.")
        #        save_and_validate_ttl(current_ontology, filename=filename)
        #        break