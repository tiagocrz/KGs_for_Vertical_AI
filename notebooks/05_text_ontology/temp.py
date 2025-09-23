import nltk
from nltk import sent_tokenize

nltk.download('punkt')

def read_text_file(file: str) -> list:
    with open(file, 'r') as file:
        text = file.read()
        sentences = nltk.sent_tokenize(text, language='portuguese')
    return sentences

prompt_c_step_1 = """Extract classes in ttl format from the following text, only return the created ttl code. 
Make sure to label all classes as of type rdfs:Class: """


prompt_c_step_2 = """Extract individuals and relations in ttl format from the following sentence, based on the given classes. 
Only return the ttl code, include the classes, individuals, and relations in this sentence. 
Make sure to label all classes as of rdfs:Class, all individuals as owl:NamedIndividual, and all properties as owl:ObjectProperty, owl:DatatypeProperty, or owl:AnnotationProperty: """

from typing import List

def clean_relations(relations, ttl_output):
    for relation in relations:
        for triple in relation:
            if triple:
                cleaned_triple = triple.strip().strip('```').strip("ttl").strip("```")
                ttl_output.append(cleaned_triple)


def gpt_results_to_ttl(relations: List, output: str):
    ttl_output = []
    clean_relations(relations, ttl_output)

    with open(output, 'w') as f:
        f.write("\n".join(ttl_output))










import requests
import json
import os
import time

def get_results_from_response(response: requests.Response) -> List[str]:
    raw_response_text = json.loads(response.text)
    if 'choices' in raw_response_text and len(raw_response_text['choices']) > 0:
        try:
            result_text = raw_response_text['choices'][0]['message']['content']
            return result_text.split('\n')
        except ValueError:
            print('Response of model is incorrect...')
    else:
        print('GPT could not identify entity relations in this sentence..')
    return []


def try_api_call(headers, text, model, prompt, ontology_info=None):
    attempts = 0
    while True:
        attempts += 1
        print('Attempt ' + str(attempts))
        if attempts > 1:
            print('Wait 5 seconds...')
            time.sleep(5)

        response = get_response(headers, text, model, prompt, ontology_info)
        status_code = response.status_code

        if status_code == 200:
            break
        elif status_code == 429:
            raise Exception("Open AI rate limit reached for requests")
        elif status_code == 400:
            raise Exception("Wrong input")
        else:
            print(f'Request failed with status code: {status_code}')
    return response


def get_response(headers, text, model, prompt, ontology_info):
    if ontology_info is None:
        message = {
            "role": "user",
            "content": f"{prompt} {text}"
        }
    else:
        message = {
            "role": "user",
            "content": f"{prompt} {text}, {ontology_info}"
        }

    print(message)


def query_gpt(text: list, method: str, model: str):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key is None:
        print("No OPENAI API key defined in the .env file. GPT-4 cannot be used...")
        return []

    headers = {"Authorization": f"Bearer {openai_api_key}"}
    relations = []

    response_1 = try_api_call(headers, text, model, prompt_c_step_1)
    for sentence in text:
        response_2 = try_api_call(headers, sentence, model, prompt_c_step_2, get_results_from_response(response_1))
        relations.append(get_results_from_response(response_2))

    print(relations)
    return relations


def main(input, output, model, method):
    if input.endswith(".txt"):
        text = read_text_file(input)
        relations = query_gpt(text, method, model)
        gpt_results_to_ttl(relations, output)

    else:
        print("Document type is not supported")
