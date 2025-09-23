from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # <-- this loads your .env

class Settings(BaseSettings):
    PROJECT_NAME: str = "Chatbot Platform"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://chatbot:chatbot123@localhost:5432/chatbot_db"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

settings = Settings()
