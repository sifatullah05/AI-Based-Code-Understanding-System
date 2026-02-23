import os
from dotenv import load_dotenv

def load_api_key():
    load_dotenv(override=True)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing in environment variables")

    return GROQ_API_KEY

