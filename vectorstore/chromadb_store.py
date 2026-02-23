from langchain_community.vectorstores import Chroma

def build_vector_db(documents, embeddings, persist_dir = "./db"):
    vector_store = Chroma.from_documents(
        documents = documents,
        embedding = embeddings,
        persist_directory = persist_dir
    )
    vector_store.persist()
    return vector_store

