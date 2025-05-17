from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Patient
import re

router = APIRouter()

def mask_phone(phone: str) -> str:
    return re.sub(r"(\+\d)(\d{3})(\d{3})(\d{2})(\d{2})", r"\1 (XXX) XXX \4 \5", phone)

@router.post("/recover/requestCode")
def recover_request_code(
    email: str = Body(...),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    masked = mask_phone(patient.mobile)
    return {
        "data": {
            "message": "Verification code sent",
            "phone_masked": masked
        }
    }
