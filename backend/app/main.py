from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.shop import router

app = FastAPI(
    title="Shopping Assistant",
    description="API for shopping assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For learning, allow all. In production, put your domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping Assistant API, Got /Docs"}