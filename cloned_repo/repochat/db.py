import os

from langchain.vectorstores import DeepLake
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import NotebookLoader, TextLoader

def vector_db(db_path, al_token, embeddings, code):
    db = DeepLake(
        dataset_path=db_path,
        token=al_token,
        embedding_function=embeddings
    )

    db.add_documents(code)

def load_to_db(repo_path):
    docs = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in files:
            if filename.startswith('.'):
                continue
            if filename == 'package-lock.json':
                continue
            file_path = os.path.join(root, filename)
            try:
                if file_path.endswith('.ipynb'):
                    loader = NotebookLoader(file_path)
                else:
                    loader = TextLoader(file_path, encoding="utf-8")
                    docs.extend(loader.load_and_split())
            except Exception as e:
                pass
            
    code_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    code = code_splitter.split_documents(docs)
    return code