import os
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS

llm = OllamaLLM(model="llama3.2:3b")
embedding = OllamaEmbeddings(model="nomic-embed-text:v1.5")

INDEX_PATH = "storage/faiss_index"

def chunk_text(text: str, source_file: str, chunk_size=1200, chunk_overlap=100):
    """
    Chunk text and add metadata about source file
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                   chunk_overlap=chunk_overlap)
    
    chunks = text_splitter.split_text(text)
    
    documents = []
    for i, chunk_text in enumerate(chunks):
        doc = Document(
            page_content=chunk_text,
            metadata={"source": source_file, "chunk_id": i}
        )
        documents.append(doc)
    
    return documents


# test chunking function
#if __name__ == "__main__":
#    with open("input/input_paper.txt", 'r', encoding='utf-8') as file:
#        content = file.read()
#    print(chunk_text(content, 'input_paper.txt')[2])


def embed_and_index(documents: list):
    """
    Embed and index Document objects (with metadata)
    """
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    
    vectorstore = FAISS.from_documents(documents, embedding)
    vectorstore.save_local(INDEX_PATH)
    print(f"Index saved at {INDEX_PATH}. {len(documents)} documents embedded and stored.")


def retrieve(input, k=5, include_metadata=False):
    vectorstore = FAISS.load_local(INDEX_PATH, embedding, 
                                   allow_dangerous_deserialization=True)
    docs = vectorstore.similarity_search(input, k=k)
    
    if include_metadata: # return list of dictionaries 
        results = []
        for doc in docs:
            results.append({
                'content': doc.page_content,
                'source': doc.metadata.get('source', 'Unknown'),
                'chunk_id': doc.metadata.get('chunk_id', 0)
            })
        return results
    else: # return list of strings
        return [doc.page_content for doc in docs]





if __name__ == "__main__":  # to keep from running when importing
    input_txt_folder = "input/inputtxt"

    # Process all txt files 
    all_documents = []
    for filename in os.listdir(input_txt_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_txt_folder, filename)
            print(f"Processing {filename}...")

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                documents = chunk_text(content, filename)
                all_documents.extend(documents)
                print(f"Added {len(documents)} documents from {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if all_documents:
        print(f"Total documents: {len(all_documents)}")
        embed_and_index(all_documents)
    else:
        print("No documents to index")