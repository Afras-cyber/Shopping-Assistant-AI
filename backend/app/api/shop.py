from fastapi import APIRouter
from app.models.schemas import ShopRequest, ShopResponse
from app.agents.team import graph

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "message": "Shop API is running"}

@router.post("/shop",response_model=ShopResponse)
def shop(request: ShopRequest):
    result = graph.invoke({
        "topic":request.topic,
        "attempts":0,
        "feedback":"",
        "approved":False,
        "budget":0,
        "plan":"",
        "research":"",
        "recommendation":""
    })
    return ShopResponse(
        recommendation=result["recommendation"],
        budget=result["budget"],
        attempts=result["attempts"]
    )