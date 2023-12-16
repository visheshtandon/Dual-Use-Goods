# Importing required packages
import os, logging

from dotenv import load_dotenv

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS


# Importing PDF Loader Module
from components.PDFLoader import PDFLoader

from components.ChunkDocuments import ChunkDocuments

from components.CreateorGetEmbedding import CreateOrGetEmbeddings

def LoadPDFDocuments():
    # documents = PDFLoader(os.path.join(os.path.dirname(__file__), "assets/data/pdf")).Load_Files()[67:70]
    documents = PDFLoader(os.path.join(os.path.dirname(__file__), "assets/data/pdf")).Load_Files()
    # documents = PDFLoader(os.path.join(os.path.dirname(__file__), "assets/data/pdf")).Load_Files()
    print("\nDocument: ", documents)
    return documents

if __name__ == "__main__":

    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    print("\nOPENAI_API_KEY: ", OPENAI_API_KEY)

    # Loading PDF Documents
    pdf_documents = LoadPDFDocuments()

    # Chunk Documents within 4000 Token Character Limit
    chunked_documents = ChunkDocuments(pdf_documents)
    print("\nChunked Documents: ", chunked_documents)

    # Get Embedding
    # vectordb = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db")
    vectordb = CreateOrGetEmbeddings(documents=chunked_documents, embeddings=OpenAIEmbeddings(), persist_directory=os.path.join(os.path.dirname(__file__), "database"))

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k":2})
    # create a chain to answer questions
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
    query = "Find out all dual goods from section List of goods and technologies referred to in Article 3b(1)"
    result = qa({"query": query})

    print("\nVector DB: ", vectordb)