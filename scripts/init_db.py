# scripts/init_db.py
from app.db.session import engine, SessionLocal
from app.db.models import Base, User
from app.core.security import hash_password

print("📌 Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")

# Add test user
db = SessionLocal()
test_email = "testuser@example.com"
test_password = "test123"
hashed_pw = hash_password(test_password)

if not db.query(User).filter(User.email == test_email).first():
    user = User(email=test_email, hashed_password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"👤 Test user added (email: {test_email} | password: {test_password})")
else:
    print("👤 Test user already exists")
db.close()
