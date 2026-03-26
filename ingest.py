import uuid
import os
import shutil
from data_loader.loader import clone_repo, load_repo_python_files
from data_loader.splitter import split_documents
from embedding.embedding_model import huggingface_embedding
from vectorstore.chromadb_store import build_vector_db


def ingestion_repo(repo_url: str):
    repo_id = str(uuid.uuid4())
    repo_path = f"repos/{repo_id}"
    db_path = f"vector_db/{repo_id}"
    
    # Create directories if not exist
    os.makedirs("repos", exist_ok=True)
    os.makedirs("vector_db", exist_ok=True)
    
    # Clean up if already exists
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    print(f"📦 Cloning repo: {repo_url}")
    clone_repo(repo_url, repo_path)
    
    print(f"📄 Loading Python files...")
    docs = load_repo_python_files(repo_path)
    print(f"✅ Loaded {len(docs)} documents")
    
    if len(docs) == 0:
        raise Exception("No Python files found in repository")
    
    print(f"✂️ Splitting documents...")
    chunks = split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks")
    
    print(f"🔧 Creating embeddings...")
    embeddings = huggingface_embedding()
    
    print(f"💾 Building vector database...")
    try:
        vector_db = build_vector_db(
            documents=chunks,
            embeddings=embeddings,
            persist_dir=db_path
        )
        print(f"✅ Vector DB created successfully at {db_path}")
    except Exception as e:
        print(f"❌ Vector DB creation failed: {e}")
        raise
    
    return {
        "repo_id": repo_id,
        "vector_db_path": db_path
    }