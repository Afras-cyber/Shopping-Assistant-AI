from pinecone import Pinecone, ServerlessSpec
from langchain_ollama import OllamaEmbeddings
from app.core.config import settings
import time

# 1. Make embeddings with Ollama on your Mac
embeddings = OllamaEmbeddings(model="nomic-embed-text")

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# 2. Professional check: Only create if it does NOT exist
if settings.PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=settings.PINECONE_INDEX_NAME,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )
    while not pc.describe_index(settings.PINECONE_INDEX_NAME).status['ready']:
        time.sleep(1)

index = pc.Index(settings.PINECONE_INDEX_NAME)

def search_products(query: str, top_k: int = 3):
    """Search Pinecone memory, return list of product texts"""
    # FIX: Turn text into numbers first, then search with numbers
    vector = embeddings.embed_query(query)
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)
    texts = []
    for m in results["matches"]:
        texts.append(m["metadata"]["text"])
    return texts

def upload_product(product_id: str, text: str, metadata: dict):
    """Upload one product to Pinecone memory"""
    # FIX: Turn text into numbers first, then upload numbers
    vector = embeddings.embed_query(text)
    index.upsert(vectors=[{"id": product_id, "values": vector, "metadata": metadata}])