from fastapi import FastAPI
from app.api import auth, projects, chat
from app.db import models
from app.db.session import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot Platform API")

# Include routers
app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router)  # already has prefix="/projects"
app.include_router(chat.router)      # already has prefix="/chats"

@app.get("/")
def root():
    return {"msg": "Chatbot Platform API is running!"}
