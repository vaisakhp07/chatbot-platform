from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.database import get_db, create_tables  # Updated import path
from app.api import auth, projects, chat, files
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()

# Create tables on startup
create_tables()

app = FastAPI(title="Chatbot Platform API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(files.router, prefix="/api/files", tags=["files"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/")
async def root():
    return {"message": "Chatbot Platform API"}

# Test database connection
@app.get("/api/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        # Try to query something simple
        result = db.execute("SELECT 1")
        return {"database": "connected", "test_query": "success"}
    except Exception as e:
        return {"database": "error", "error": str(e)}