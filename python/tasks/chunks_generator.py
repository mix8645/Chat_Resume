import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
resume_path = os.path.join(project_root, 'doc', 'resume.txt')

loader = TextLoader(resume_path, encoding="utf-8")

documents = loader.load() 

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=40
)

chunks = text_splitter.split_documents(documents)