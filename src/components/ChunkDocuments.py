from langchain.text_splitter import CharacterTextSplitter

def ChunkDocuments(documents):
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunked_documents = text_splitter.split_documents(documents)
    return chunked_documents