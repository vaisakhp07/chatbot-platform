# init_db.py
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine
from app.db.models import Base

def init_database():
    try:
        # Drop all tables (clean start)
        Base.metadata.drop_all(bind=engine)
        print("Dropped existing tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database()