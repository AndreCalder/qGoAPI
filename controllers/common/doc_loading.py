from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_community.document_loaders import UnstructuredCSVLoader
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain.docstore.document import Document


def load_doc(file_ext:str, uploaded_file) -> Document:
    if file_ext.lower() == 'txt':
        doc = TextLoader(uploaded_file, encoding='utf-8').load()
    elif file_ext.lower() == 'docx' | file_ext.lower() == 'doc': 
        doc = UnstructuredWordDocumentLoader(uploaded_file, encoding='utf-8').load()
    elif file_ext.lower() == 'pdf':
        doc = PyPDFLoader(uploaded_file).load()
    elif file_ext.lower() == 'pptx' | file_ext.lower() == 'ppt':
        doc = UnstructuredPowerPointLoader(uploaded_file, encoding='utf-8').load()
    elif file_ext.lower() == 'csv': 
        doc = UnstructuredCSVLoader(uploaded_file, encoding='utf-8').load()
    elif file_ext.lower() == 'Excel':
        doc = UnstructuredExcelLoader(uploaded_file, encoding='utf-8').load()
    else: 
        doc = None
    return doc


def load_docs():
    pass