from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db import models
from app.schemas import ChatCreate, ChatResponse
from app.api.auth import get_current_user

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Replace with real AI integration later
    response_text = f"Echo: {chat.message}"
    new_chat = models.Chat(
        message=chat.message,
        response=response_text,
        user_id=current_user.id,
        project_id=chat.project_id
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

@router.get("/", response_model=List[ChatResponse])
def list_chats(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Chat).filter(models.Chat.user_id == current_user.id).all()
