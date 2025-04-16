from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from helper.pdf import save_online_pdf
import os
import tracemalloc
import asyncio

tracemalloc.start()

# Store Embeddings in AstraDB Vector Store (Fresh Data)
async def store_vectors():

    ASTRA_DB_API_ENDPOINT = input("AstraDB API Endpoint: ")
    ASTRA_DB_APPLICATION_TOKEN = input("AstraDB Application Token: ")
    ASTRA_DB_NAMESPACE = input("AstraDB Namespace: ")


    pdf_path = None
    is_local = input("Is the file local? Y/N: ").upper()
    
    if (is_local == "Y"):
        file_name = input("Name of the file: ")

        # Ensure the PDF file exists
        pdf_path = f"./sources/{file_name}.pdf"

    elif (is_local == "N"):
        pdf_url = input("Enter pdf url:")
        pdf_path = save_online_pdf(pdf_url)

    else:
        return "Invalid input"

    # Error handling if file is not found
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    pdf_loader = PyPDFLoader(pdf_path)  
    documents = pdf_loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model)

    vectorstore = AstraDBVectorStore(
        collection_name="main_v2",
        embedding=embeddings,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_NAMESPACE,
    )    

    vectorstore.add_documents(documents=docs)

    return "Vectors stored successfully."

if __name__ == "__main__":
    asyncio.run(store_vectors())
    