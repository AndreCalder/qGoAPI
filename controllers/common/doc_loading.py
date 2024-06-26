from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredCSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.docstore.document import Document

def load_doc(file_ext:str, uploaded_file) -> Document:
   
   match file_ext.lower():
        case 'txt': 
            doc = TextLoader(uploaded_file, encoding='utf-8').load()
        case 'docx' | 'doc': 
            doc = UnstructuredWordDocumentLoader(uploaded_file, encoding='utf-8').load()
        case 'pdf':
            doc = PyPDFLoader(uploaded_file).load()
        case 'pptx' | 'ppt':
            doc = UnstructuredPowerPointLoader(uploaded_file, encoding='utf-8').load()
        case 'csv': 
            doc = UnstructuredCSVLoader(uploaded_file, encoding='utf-8').load()
        case 'Excel':
            doc = UnstructuredExcelLoader(uploaded_file, encoding='utf-8').load()
        case _: 
            doc = None

   return doc


def load_docs():
    pass