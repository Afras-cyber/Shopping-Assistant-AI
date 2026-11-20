# backend/scripts/ingest_pinecone.py - Run once to fill memory
import sys
from pathlib import Path
# Add backend/ folder to Python's search path
# __file__ = .../backend/scripts/ingest_pinecone.py
# .parent = .../backend/scripts
# .parent.parent = .../backend  <- this is where app/ lives
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.tools.pinecone_memory import upload_product

products = [
    {"id": "1", "name": " 【entity-Dell¦canonical_name=Dell】 Inspiron 15, i5, 8GB RAM, 512GB", "price": 145000, "type": "laptop", "use": "coding, study"},
    {"id": "2", "name": " HP Pavilion 15, i5, 16GB RAM, 512GB", "price": 185000, "type": "laptop", "use": "coding, heavy"},
    {"id": "3", "name": " Lenovo IdeaPad Slim 3, i3, 8GB RAM", "price": 115000, "type": "laptop", "use": "study, browsing"},
    {"id": "4", "name": " Sony WH-CH520 Headphones", "price": 12500, "type": "headphones", "use": "music, calls"},
    {"id": "5", "name": " Logitech B170 Mouse", "price": 3500, "type": "mouse", "use": "office"},
]

for p in products:
    text = f"{p['name']} price {p['price']} LKR type {p['type']} use {p['use']}"
    upload_product(p['id'], text, {
        "name": p['name'], 
        "price": p['price'], 
        "type": p['type'], 
        "text": text
    })
    print(f"Uploaded: {p['name']}")

print("Done. Pinecone memory ready.")