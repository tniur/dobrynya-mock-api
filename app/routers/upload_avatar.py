from fastapi import APIRouter, File, UploadFile, HTTPException, Query
import os
from uuid import uuid4
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey


router = APIRouter()

AVATAR_DIR = "app/static/avatars"

@router.post("/uploadAvatar")
async def upload_avatar(
    patient_key: str = Query(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    key_entry = db.query(PatientKey).filter_by(key=patient_key).first()
    if not key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{file_extension}"
    file_path = os.path.join(AVATAR_DIR, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    patient = key_entry.patient
    patient.avatar_path = f"avatars/{filename}"
    db.commit()

    return {
        "success": True,
        "avatar_url": patient.avatar_path
    }
