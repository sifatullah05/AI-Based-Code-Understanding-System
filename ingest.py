import uuid


from data_loader.loader import clone_repo, load_repo_python_files
from data_loader.splitter import split_documents
from embedding.embedding_model import huggingface_embedding
from vectorstore.chromadb_store import build_vector_db


def ingestion_repo(repo_url: str):
    repo_id = str(uuid.uuid4())
    repo_path = f"repos/{repo_id}"
    db_path = f"vector_db/{repo_id}"

    clone_repo(repo_url,repo_path)

    docs = load_repo_python_files(repo_path)
    chunks = split_documents(docs)
    embeddings = huggingface_embedding()
    vector_db = build_vector_db(
        documents=chunks,
        embeddings=embeddings,
        persist_dir=db_path
    )
    return {
        "repo_id": repo_id,
        "vector_db_path":db_path
    }










   
