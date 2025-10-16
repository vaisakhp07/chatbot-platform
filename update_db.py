import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import engine
from app.db.models import Base

def update_database():
    try:
        # Drop and recreate tables (for development)
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables updated successfully!")
    except Exception as e:
        print(f"❌ Error updating database: {e}")

if __name__ == "__main__":
    update_database()