from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Project schemas - UPDATED: Added model field
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    model: Optional[str] = "gpt-3.5-turbo"  # Added this field

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Chat schemas
class ChatRequest(BaseModel):
    message: str
    project_id: int

class ChatResponse(BaseModel):
    response: str

class ChatMessageResponse(BaseModel):
    id: int
    message: str
    response: Optional[str]
    message_type: str
    timestamp: datetime

    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse  # Add this line

class TokenData(BaseModel):
    email: Optional[str] = None

# File schemas
class FileBase(BaseModel):
    filename: str
    content_type: str

class FileResponse(FileBase):
    id: int
    project_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True