from app.db.session import SessionLocal
from app.db import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db = SessionLocal()

# Change email/password if needed
hashed = pwd_context.hash("test123")
user = models.User(email="test@example.com", hashed_password=hashed)

db.add(user)
db.commit()
db.refresh(user)

print("✅ User created:", user.id, user.email)
