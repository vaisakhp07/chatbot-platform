# Location: app/api/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.api.auth import get_current_user  # Your JWT dependency

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

# Get all projects for logged-in user
@router.get("/")
def get_projects(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = db.query(models.Project).filter(models.Project.owner_id == current_user.id).all()
    return projects

# Create a new project
@router.post("/")
def create_project(title: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_project = models.Project(title=title, owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project
