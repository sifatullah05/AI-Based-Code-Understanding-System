from langchain_text_splitters import RecursiveCharacterTextSplitter, Language



def split_documents(documents):

    document_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=500,
        chunk_overlap=50
    )

    splitter = document_splitter.split_documents(documents)

    return splitter