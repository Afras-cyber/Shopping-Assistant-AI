from pydantic import BaseModel

class ShopRequest(BaseModel):
    topic: str
   
class ShopResponse(BaseModel):
    recommendation: str
    budget: int
    attempts: int
