import os
from langchain_chroma import Chroma 

def build_vector_db(documents, embeddings, persist_dir="./db"):
    if not documents:
        raise Exception("No documents to build vector database")
    
    # Create directory if not exists
    os.makedirs(persist_dir, exist_ok=True)
    
    print(f"Building vector DB with {len(documents)} documents at {persist_dir}")
    
    try:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_dir
        )
        
        
        # Chroma.from_documents automatically persists
        print(f"Vector DB created successfully")
        
        return vector_store
        
    except Exception as e:
        print(f"Error creating vector DB: {e}")
        raise
