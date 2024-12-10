import csv

import chromadb
from chromadb.utils import embedding_functions

def knowlege_base_update(company_name):
    documents = []
    metadatas = []
    ids = []
    id = 1
    file_name=["company_website_details.txt","main_points.txt"]
    for i in file_name:
        with open("knowlege_base/"+company_name+"/"+i, "r") as file:
            documents.append(file.read())
            metadatas.append({"item_id": company_name+"/"+i})
            ids.append(str(id))
            id+=1    
    # Instantiate chromadb instance. Data is stored on disk (a folder named 'my_vectordb' will be created in the same folder as this file).
    chroma_client = chromadb.PersistentClient(path="companies_kb_vdb")
    google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key="AIzaSyC-T3xSPDbha8Q4jaByQbef7i0gk0aqp5k")

    # Use this to delete the database
    # chroma_client.delete_collection(name="my_collection")

    # Create the collection, aka vector database. Or, if database already exist, then use it. Specify the model that we want to use to do the embedding.
    collection = chroma_client.get_or_create_collection(name="my_collection", embedding_function=google_ef)
    # Add all the data to the vector database. ChromaDB automatically converts and stores the text as vector embeddings. This may take a few minutes.
    collection.update(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    results = collection.query(
        query_texts=["100xengineers"],
        n_results=5,
        include=['documents', 'distances', 'metadatas']
    )
    return results
tmp= knowlege_base_update("100xengineers")
print(tmp)