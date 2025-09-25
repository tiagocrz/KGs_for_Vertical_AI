# Read ontology txt file
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from src.txt_ontology_learning import save_and_validate_ttl

with open('results/ontologies/text/text_ontology.txt', 'r') as file:
    ontology = file.read()

save_and_validate_ttl(ontology, filename="text_ontology.ttl")