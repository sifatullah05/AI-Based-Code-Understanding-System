from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language

def clone_repo(repo_url, repo_path):
    Repo.clone_from(repo_url, repo_path)

def load_repo_python_files(repo_path):
    loader = GenericLoader.from_filesystem(
        repo_path,
        glob="**/*",
        suffixes=[".py"],
        parser=LanguageParser(
            language=Language.PYTHON,
            parser_threshold=500
        )
    )

    return loader.load()