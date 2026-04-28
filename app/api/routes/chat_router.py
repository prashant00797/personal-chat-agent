from fastapi import APIRouter
from app.api.api_service.chat_service import ai_reponse
from app.schema.chat_schema import ChatRequest

router = APIRouter(tags=["Chat"])

@router.post("/chat")
async def user_message(user_request:ChatRequest):
    return await ai_reponse(user_request)



  