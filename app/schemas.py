from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ----- User Schemas -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# ----- Project Schemas -----
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int

    class Config:
        orm_mode = True

# ----- Chat Schemas -----
class ChatCreate(BaseModel):
    message: str
    project_id: Optional[int] = None

class ChatResponse(BaseModel):
    id: int
    message: str
    response: str
    user_id: int
    project_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True
