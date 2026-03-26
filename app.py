from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_chroma import Chroma
from ingest import ingestion_repo
from embedding.embedding_model import huggingface_embedding
from retriever.retriever import get_retriever
from llm.groq_model import build_chat_model
from chains.rag_chain import build_rag_chain
from chains.prompt import SYSTEM_PROMPT
from config import load_api_key
from utils.memory import store
import os
import json
from functools import lru_cache
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # React dev server default (vite)
    "http://localhost:3000",  # React dev server (CRA)
]
app = FastAPI(title="Github Source Code Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------
# EMBEDDING & LLM SETUP
# ----------------------------
embeddings = huggingface_embedding()
api_key = load_api_key()
llm = build_chat_model(api_key)

# ----------------------------
# INDEX STATUS - TRACK INDEXING
# ----------------------------
STATUS_FILE = "backend_status.json"

def save_status():
    """Save current indexing status to JSON file"""
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(INDEX_STATUS, f)
        print(f"Status saved: {INDEX_STATUS}")
    except Exception as e:
        print(f"Error saving status: {e}")

def load_status():
    """Load indexing status from JSON file"""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                status = json.load(f)
            print(f"Loaded status: {status}")
            # Ensure all required keys exist
            return {
                "indexing": status.get("indexing", False),
                "repo_id": status.get("repo_id", None)
            }
        except Exception as e:
            print(f"Error loading status: {e}")
    return {"indexing": False, "repo_id": None}

# GLOBAL INDEX STATUS
INDEX_STATUS = load_status()

@lru_cache(maxsize=100)
def get_cached_vector_store(repo_id: str):
    db_path = f"vector_db/{repo_id}"
    print(f"🔍 Looking for vector store at: {db_path}")
    
    if not os.path.isdir(db_path):
        print(f"Directory does not exist: {db_path}")
        # Show what's available
        if os.path.isdir("vector_db"):
            print(f"Available repos: {os.listdir('vector_db')}")
        else:
            print("vector_db folder doesn't exist!")
        return None
    
    print(f"Loading vector store from {db_path}")
    
    try:
        vector_store = Chroma(
            persist_directory=db_path,
            embedding_function=embeddings
        )
        print(f"Vector store loaded successfully")
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None

# ----------------------------
# REQUEST MODELS
# ----------------------------
class Ingest_Request(BaseModel):
    repo_url: str

class Chat_Request(BaseModel):
    repo_id: str
    question: str
    session_id: str

# ----------------------------
# INGEST ENDPOINT
# ----------------------------
@app.post("/ingest", status_code=201)
def ingest_repo(request: Ingest_Request):
    if INDEX_STATUS.get("indexing", False):
        raise HTTPException(
            status_code=400,
            detail=f"Another repository is currently being indexed: {INDEX_STATUS.get('repo_id')}"
        )
    
    try:
        # Update index status before starting
        INDEX_STATUS["indexing"] = True
        INDEX_STATUS["repo_id"] = request.repo_url
        save_status()

        # Actual ingestion
        result = ingestion_repo(request.repo_url)

        # Reset index status after completion
        INDEX_STATUS["indexing"] = False
        INDEX_STATUS["repo_id"] = None
        save_status()

        return {
            "message": "Repository ingested successfully",
            "repo_id": result["repo_id"]
        }
    except Exception as e:
        # Reset index status if error occurs
        INDEX_STATUS["indexing"] = False
        INDEX_STATUS["repo_id"] = None
        save_status()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
def chat_with_repo(request: Chat_Request):
    try:
        print(f"Chat request for repo_id: {request.repo_id}")
        print(f"Question: {request.question}")
        
        vector_store = get_cached_vector_store(request.repo_id)

        if vector_store is None:
            print(f"Vector store not found for repo_id: {request.repo_id}")
            raise HTTPException(status_code=404, detail="Repository not found")

        # Create retriever
        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Test retrieval with invoke method
        test_docs = retriever.invoke(request.question)
        print(f"Retrieved {len(test_docs)} documents")
        
        if len(test_docs) == 0:
            print("WARNING: No documents retrieved! Vector store might be empty.")
            return {"answer": "I couldn't find any relevant code in the repository. Please make sure the repository was ingested correctly."}
        
        # Build RAG chain
        rag_chain = build_rag_chain(
            retriever,
            llm,
            system_prompt=SYSTEM_PROMPT
        )

        # Get response
        response = rag_chain.invoke(
            {"question": request.question},
            config={"configurable": {"session_id": request.session_id}}
        )

        print(f"Response generated successfully")
        return {"answer": str(response)}

    except AttributeError as e:
        print(f"Attribute Error: {e}")
        raise HTTPException(status_code=500, detail=f"Method not found: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# DELETE CHAT HISTORY
# ----------------------------
@app.delete("/chat/{session_id}")
def delete_chat(session_id: str):
    if session_id in store:
        del store[session_id]
        return {"message": "Chat history successfully deleted"}
    raise HTTPException(status_code=404, detail="Session ID not found")

# ----------------------------
# INDEX STATUS CHECK ENDPOINT
# ----------------------------
@app.get("/status")
def get_index_status():
    return INDEX_STATUS

