from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine, Base
from app.db.models import User
from app.core.security import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_test_user():
    db: Session = SessionLocal()

    # Check if user already exists
    existing = db.query(User).filter(User.email == "demo@example.com").first()
    if existing:
        print("User already exists:", existing.email)
        return

    # Hash password
    hashed_pw = get_password_hash("password123")

    # Create user
    user = User(email="demo@example.com", hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    print("✅ Created test user:", user.email)

if __name__ == "__main__":
    create_test_user()
