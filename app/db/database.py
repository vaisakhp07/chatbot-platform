from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# We'll initialize these lazily when needed
_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            # For build phase, use SQLite that won't fail
            _engine = create_engine("sqlite:///./temp.db", connect_args={"check_same_thread": False})
        else:
            # Production - use PostgreSQL
            _engine = create_engine(DATABASE_URL)
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

# Dependency to get DB session
def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

# Create all tables - only if we have a real database
def create_tables():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
        Base.metadata.create_all(bind=get_engine())
        print("✅ Database tables created successfully")
    else:
        print("⚠️  Skipping table creation - no PostgreSQL DATABASE_URL available")
