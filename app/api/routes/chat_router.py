from fastapi import APIRouter, Request
from app.api.api_service.chat_service import ai_reponse
from app.core.limiter import limiter
from app.schema.chat_schema import ChatRequest

router = APIRouter(tags=["Chat"])


@router.post("/chat")
@limiter.limit("30/minute")
async def user_message(user_request:ChatRequest,request:Request):
    return await ai_reponse(user_request,request )



  