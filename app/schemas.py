# app/schemas.py
from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatCreate(BaseModel):
    message: str
    project_id: int

class ChatResponse(BaseModel):
    id: int
    message: str
    response: str
    user_id: int
    project_id: int

    class Config:
        orm_mode = True
