from rag_tools import retrieve
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import os

llm = OllamaLLM(model="llama3.2:3b")
embedding = OllamaEmbeddings(model="nomic-embed-text:v1.5")


def generate_response(question, k=5):
    """
    Retrieve relevant chunks and generate answer
    """
    retrieved_chunks = retrieve(question, k=k)
    
    prompt = f"""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the user question
        - Include all information that is relevant to the question
        - Keep your response clear and concise. Aim for 3 sentences or less, but you can include more if needed to cover all the relevant information
        - If the answer is not in the context, say "I don't know"
        - Do not add information that isn't supported by the context
    Context:
    {retrieved_chunks}

    Question: {question}"""
    
    response = llm.invoke(prompt)
    return response


def generate_response_with_sources(question, k=5):
    retrieved_results = retrieve(question, k=k, include_metadata=True)
    
    # Create context with source attribution
    context_parts = []
    for i, result in enumerate(retrieved_results, 1):
        context_parts.append(f"[Source {i}: {result['source']}]\n{result['content']}")
    
    context = "\n\n".join(context_parts)
    
    prompt = f"""You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the user question. Each piece of context includes its source.
        - Include all information that is relevant to the question
        - When possible, mention which file supports your answer
        - Keep your response clear and concise. Aim for 3 sentences or less, but you can include more if needed to cover all the relevant information
        - If the answer is not in the context, say "I don't know"
        - Do not add information that isn't supported by the context
    Context:
    {context}

    Question: {question}"""
    
    response = llm.invoke(prompt)
    return response

questions = [
    "What are the specific goals of Granter?",
    "what does the pilot 3 project consist of?",
    "What is the maximum public support rate available for start-ups, spin-offs, or co-promotion projects introducing innovative products, processes, or equipment?",
    "What are the types of eligible expenses covered under this notice for projects in the transformation of fishery and aquaculture products?",
    "According to this document, what is the deadline for submitting projects to the “Atlantic Deep-Sea Mining Innovation Grant?"
]

#questions = [
#    'what are some considerations for choosing between RAG and Fine-Tuning?',
#    'what is RAG?',
#    'how does fine-tuning work?',
#    'what are knowledge graphs used for?'
#]

results_dir = "approaches/01_vector_rag/results"
os.makedirs(results_dir, exist_ok=True) # create/check results folder
output_file = os.path.join(results_dir, "vector_rag_results.txt")

for i,question in enumerate(questions):
    print(f'Generating answer for question {i}...')
    answer = generate_response(question, k=3)

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n")
        f.write("\n\n" + "-" * 80 + "\n\n")

with open(output_file, 'a', encoding='utf-8') as f:
    f.write(f"\n\nANSWERS WITH SOURCE\n")

for i, question in enumerate(questions):
    print(f'Generating answer for question {i} with source...')
    answer = generate_response_with_sources(question, k=3)

    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(f"Question: {question}\n")
        f.write(f"Answer(with source): {answer}\n")
        f.write("\n\n" + "-" * 80 + "\n\n")