import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(key, default=None):
    """
    Priority:
    1. Streamlit secrets (Streamlit Cloud)
    2. Environment variables (.env file or system env)
    3. Default value
    """
    try:
        return st.secrets.get(key)
    except (AttributeError, FileNotFoundError):
        print('Could not find secrets')
        return os.getenv(key, default)

OPENAI_API_KEY = get_secret('OPENAI_API_KEY')
ENCRYPTION_KEY = get_secret('ENCRYPTION_KEY')
FAMILY_PASSWORD = get_secret('FAMILY_PASSWORD')

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file")

if not ENCRYPTION_KEY:
    raise ValueError("❌ ENCRYPTION_KEY not found in .env file")

if not FAMILY_PASSWORD:
    raise ValueError("❌ FAMILY_PASSWORD not found in .env file")

DATA_DIR = "./data"
ENCRYPTED_DATA_DIR = "./encrypted_data"
CHROMA_DB_DIR = "./chroma_db"
DOC_FILE = os.path.join(DATA_DIR, "Rodzina_Karasi.docx")
ENCRYPTED_DOC_FILE = os.path.join(ENCRYPTED_DATA_DIR, "Rodzina_Karasi.docx.enc")

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
VECTOR_SEARCH_K = 5
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0