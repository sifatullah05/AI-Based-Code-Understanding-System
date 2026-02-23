from langchain_groq import ChatGroq

def build_chat_model(api_key):
    chat_model =  ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        api_key=api_key
    )
    return chat_model