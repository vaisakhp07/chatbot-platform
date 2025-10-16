import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import User
from app.core.security import get_password_hash

def create_test_user():
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@example.com").first()
        if existing_user:
            print("ℹ️ Test user already exists")
            return
        
        # Create test user
        test_user = User(
            email="test@example.com",
            name="Test User",
            password=get_password_hash("password123")
        )
        db.add(test_user)
        db.commit()
        print("✅ Test user created successfully!")
        print("   Email: test@example.com")
        print("   Password: password123")
        
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()