from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from uuid import uuid4
import base64
import os

router = APIRouter()

AVATAR_DIR = "app/static/avatars"

class AvatarUploadRequest(BaseModel):
    patient_key: str
    image_base64: str

@router.post("/uploadPatientAvatar")
def upload_patient_avatar(data: AvatarUploadRequest, db: Session = Depends(get_db)):

    key_entry = db.query(PatientKey).filter_by(key=data.patient_key).first()
    if not key_entry or not key_entry.patient:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    patient = key_entry.patient

    try:
        image_data = base64.b64decode(data.image_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")

    filename = f"avatar_{uuid4().hex}.jpeg"
    filepath = os.path.join(AVATAR_DIR, filename)

    os.makedirs(AVATAR_DIR, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(image_data)

    patient.avatar_path = f"avatars/{filename}"
    db.commit()

    return {
        "success": True,
        "avatar_url": patient.avatar_path,
        "message": "JPEG avatar uploaded successfully"
    }
