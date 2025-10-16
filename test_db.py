# test_db.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import User
from sqlalchemy import text

def test_connection():
    db = SessionLocal()
    try:
        # Try a simple query
        result = db.execute(text("SELECT version()"))
        version = result.fetchone()
        print("✅ PostgreSQL version:", version[0])
        
        # Check current database
        result = db.execute(text("SELECT current_database()"))
        db_name = result.fetchone()
        print("✅ Current database:", db_name[0])
        
        # Check if tables exist
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        print("✅ Tables in database:", tables)
        
        print("✅ Database connection successful!")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()