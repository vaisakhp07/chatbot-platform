from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.database import get_db
from app.api import auth, projects, chat, files
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Chatbot Platform API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    from app.db.database import create_tables
    create_tables()
    print("✅ Application startup complete - database ready")

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

# Test database connection - FIXED for SQLAlchemy 2.0
@app.get("/api/test-db")
async def test_db(db: Session = Depends(get_db)):
    try:
        # Use text() for explicit SQL in SQLAlchemy 2.0
        result = db.execute(text("SELECT 1"))
        return {"database": "connected", "test_query": "success"}
    except Exception as e:
        return {"database": "error", "error": str(e)}
