from fastapi import APIRouter
from app.services.openai_client import call_openai_response

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/")
async def chat(user_message: str):
    resp = await call_openai_response(user_message, [])
    return {"assistant": resp}
