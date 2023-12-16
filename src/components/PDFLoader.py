from langchain.document_loaders import PyPDFDirectoryLoader

class PDFLoader():
    def __init__(self, pdf_folder_path):
        self.__pdf_folder_path = pdf_folder_path
        pass

    def Load_Files(self):
        loader = PyPDFDirectoryLoader(self.__pdf_folder_path)
        documents = loader.load()
        return documents