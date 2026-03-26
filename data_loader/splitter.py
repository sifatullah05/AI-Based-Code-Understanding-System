from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

def split_documents(documents):
    if not documents:
        print("No documents to split")
        return []
    
    document_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=500,
        chunk_overlap=50
    )

    splitter = document_splitter.split_documents(documents)
    print(f"Split {len(documents)} docs into {len(splitter)} chunks")
    return splitter