# backend/app/core/config.py - Only file that reads .env
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "shop-products")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

settings = Settings()