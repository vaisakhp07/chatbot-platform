from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.session import get_db
from jose import jwt, JWTError
from app.core.config import settings

router = APIRouter(prefix="/api/projects", tags=["projects"])

def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user = db.query(models.User).filter(models.User.id == payload.get("sub")).first()
        return user
    except JWTError:
        return None

@router.post("/")
def create_project(name: str, description: str = "", db: Session = Depends(get_db), token: str = ""):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    project = models.Project(name=name, description=description, owner=user)
    db.add(project); db.commit(); db.refresh(project)
    return {"id": project.id, "name": project.name}
