from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models, database
from app.api.auth import get_current_user
from app.schemas import ChatCreate
import os
from openai import OpenAI

router = APIRouter(prefix="/chats", tags=["Chats"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chatbot_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error contacting AI: {str(e)}"

@router.get("/")
def list_chats(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Chat).filter(models.Chat.user_id == current_user.id).all()

@router.post("/")
def send_message(request: ChatCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    user_chat = models.Chat(user_id=current_user.id, project_id=request.project_id, message=request.message, sender="user")
    db.add(user_chat)
    db.commit()
    db.refresh(user_chat)

    bot_reply = chatbot_response(request.message)
    bot_chat = models.Chat(user_id=current_user.id, project_id=request.project_id, message=bot_reply, sender="bot")
    db.add(bot_chat)
    db.commit()
    db.refresh(bot_chat)

    return {"message": user_chat.message, "response": bot_chat.message}
