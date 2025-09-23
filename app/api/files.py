from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

from app.db.session import get_db
from app.db import models
from app.api.auth import get_current_user
from app.schemas import FileResponse

router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------------------------
# Upload a file to a project
# ---------------------------
@router.post("/upload", response_model=FileResponse)
def upload_file(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")

    # Save file with unique prefix to avoid name conflicts
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    new_file = models.File(
        filename=unique_filename,
        project_id=project_id,
        user_id=current_user.id
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file

# ---------------------------
# List files for a project
# ---------------------------
@router.get("/", response_model=List[FileResponse])
def list_files(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    project = db.query(models.Project).filter(
        models.Project.id == project_id,
        models.Project.owner_id == current_user.id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")

    files = db.query(models.File).filter(models.File.project_id == project_id).all()
    return files

# ---------------------------
# Download a file by ID
# ---------------------------
@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    file_record = db.query(models.File).filter(models.File.id == file_id).first()
    if not file_record:
        raise HTTPException(status_code=404, detail="File not found")

    # Only owner can download
    if file_record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to download this file")

    file_path = os.path.join(UPLOAD_DIR, file_record.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File missing on server")

    return FileResponse(file_path, filename=file_record.filename)
