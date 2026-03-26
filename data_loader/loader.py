import os
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language

def clone_repo(repo_url, repo_path):
    try:
        print(f"Cloning from {repo_url}")
        Repo.clone_from(repo_url, repo_path)
        print(f"Clone successful")
    except Exception as e:
        print(f"Clone failed: {e}")
        raise

def load_repo_python_files(repo_path):
    print(f"Looking for Python files in {repo_path}")
    
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(
            language=Language.PYTHON,
            parser_threshold=500
        )
    )

    documents = loader.load()
    print(f"Found {len(documents)} Python files")
    
    # Show first few file names
    for i, doc in enumerate(documents[:3]):
        source = doc.metadata.get('source', 'Unknown')
        print(f"   File {i+1}: {source}")
    
    return documents