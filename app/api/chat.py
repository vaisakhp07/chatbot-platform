import os
import requests
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.db.models import User, ChatMessage, Project
from app.api.auth import get_current_user
from app.schemas import ChatRequest, ChatResponse

router = APIRouter()

def get_ai_response(message: str) -> str:
    """Use OpenRouter for free AI responses"""
    try:
        # Use your actual OpenRouter key directly
        api_key = "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"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'HTTP-Referer': 'http://localhost:3000',
            'X-Title': 'Chatbot Platform'
        }
        
        data = {
            'model': 'openai/gpt-3.5-turbo',  # Free GPT-3.5 via OpenRouter
            'messages': [
                {'role': 'system', 'content': 'You are a helpful AI assistant. Provide clear, concise, and helpful responses.'},
                {'role': 'user', 'content': message}
            ],
            'max_tokens': 150
        }
        
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            error_msg = f"OpenRouter Error: {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg += f" - {error_data['error'].get('message', 'Unknown error')}"
            except:
                error_msg += f" - {response.text}"
            return error_msg
            
    except Exception as e:
        return f"Connection Error: {str(e)}"

@router.post("/send", response_model=ChatResponse)
async def send_message(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify the project belongs to the current user
    project = db.query(Project).filter(
        Project.id == chat_request.project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Save user message to database
    user_message = ChatMessage(
        user_id=current_user.id,
        project_id=chat_request.project_id,
        message=chat_request.message,
        message_type="user"
    )
    db.add(user_message)
    db.flush()

    # Generate AI response using OpenRouter
    ai_response = get_ai_response(chat_request.message)

    # Save AI response to database
    ai_message = ChatMessage(
        user_id=current_user.id,
        project_id=chat_request.project_id,
        message=ai_response,
        message_type="assistant",
        response=ai_response
    )
    db.add(ai_message)
    
    # Commit both messages
    db.commit()

    return ChatResponse(response=ai_response)

@router.get("/history/{project_id}")
async def get_chat_history(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify project belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get chat history for this project
    messages = db.query(ChatMessage).filter(
        ChatMessage.project_id == project_id,
        ChatMessage.user_id == current_user.id
    ).order_by(ChatMessage.timestamp.asc()).all()

    return [
        {
            "id": msg.id,
            "message": msg.message,
            "response": msg.response,
            "message_type": msg.message_type,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]