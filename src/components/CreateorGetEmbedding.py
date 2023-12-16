import os, pickle, faiss, json
from langchain.vectorstores import Chroma
from langchain.vectorstores import FAISS

def CreateOrGetEmbeddings(documents, embeddings, persist_directory):
    persist_directory = os.path.join(os.getcwd(), persist_directory)
    checkDirectoryExists = os.path.isdir(persist_directory)
    # checkDirectoryExists = os.path.isdir(os.path.join(os.getcwd(), persist_directory))
    print("\nCheck Directory Exists:", checkDirectoryExists, os.path.join(os.getcwd(), persist_directory))
    if(checkDirectoryExists):
        # vectordb = Chroma(embedding_function=embeddings, persist_directory=persist_directory)
        with open(os.path.join(persist_directory, "vectordb.pkl"), "rb") as f:
            vectordb = pickle.load(f)
    else:
        vectordb = FAISS.from_documents(documents=documents, embedding=embeddings)
        # vectordb = Chroma.from_documents(documents=documents, embedding=embeddings)
        faiss.write_index(vectordb.index, "docs.index")
        vectordb.index = None
        # vdb = {"s": vectordb}
        print("\nvectordb: ", vectordb, "Faiss: ", faiss)
        os.mkdir(persist_directory)
        # with open("vectordb.json", "w") as outfile:
        #     json.dump(vdb, outfile)
        # with open('vectordb.json', "wb") as f:
        #     f.write(vdb)
        with open("vectorstore.pkl", "wb") as f:
            pickle.dump(vectordb, f)

    return vectordb