from fastapi import FastAPI
from app.api import auth, projects, chat
from app.db import models
from app.db.session import engine

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Chatbot Platform")

# Register routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"msg": "Chatbot Platform API is running!"}
