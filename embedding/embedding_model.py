from langchain_huggingface import HuggingFaceEmbeddings

def huggingface_embedding():
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
    return embeddings