from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma

from ingest import ingestion_repo
from embedding.embedding_model import huggingface_embedding
from retriever.retriever import get_retriever
from llm.groq_model import build_chat_model
from chains.prompt import SYSTEM_PROMPT
from chains.rag_chain import build_rag_chain
from config import load_api_key
from utils.memory import store
import os


app = FastAPI(title="Github Source Code Analysis")


embeddings = huggingface_embedding()
api_key = load_api_key()
llm = build_chat_model(api_key)

class Ingest_Request(BaseModel):
    repo_url: str

class Chat_Request(BaseModel):
    repo_id: str
    question: str
    session_id: str


@app.post("/ingest", status_code=201)
def ingest_repo(request: Ingest_Request):
     try:
          result = ingestion_repo(request.repo_url)
          return {
               "message":"Repository ingested successfully",
               "repo_id": result["repo_id"]
          }
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))




@app.post("/chat")
def chat_with_repo(request: Chat_Request):
     
     db_path = f"vector_db/{request.repo_id}"

     if not os.path.isdir(db_path):
          raise HTTPException(
               status_code=404,
               detail= "Repository not found"
          )
     

     try:
          
          vector_store = Chroma(
               persist_directory= db_path,
               embedding_function=embeddings
          )

          retriever = get_retriever(vector_store)

          rag_chain = build_rag_chain(retriever, llm)

          response = rag_chain.invoke(
               {
                    "question": request.question
               },
               config={"configurable": {"session_id": request.session_id}}
          )
          
          return {"answer": response}
     except Exception as e:
          raise HTTPException(status_code=500, detail=str(e))
     

@app.delete("/chat/{session_id}")
def delete_chat(session_id:str):
    if session_id in store:
         del store[session_id]
         return {"message": "Chat history successfully deleted"}
    raise HTTPException(
         status_code=404,
         detail="Session ID not found"
    )

    
    




