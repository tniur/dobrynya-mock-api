from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Patient, PatientKey
import uuid

router = APIRouter()

class ConfirmRegisterRequest(BaseModel):
    email: str
    password: str
    mobile: str
    code: str

@router.post("/auth/register/confirmCode")
def register_confirm_code(
    req: ConfirmRegisterRequest,
    db: Session = Depends(get_db)
):
    if req.code != "123456":
        raise HTTPException(status_code=401, detail="Invalid verification code")

    existing_patient = db.query(Patient).filter(Patient.email == req.email).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_patient = Patient(
        email=req.email,
        password=req.password,
        mobile=req.mobile
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    key_entry = PatientKey(patient_id=new_patient.id, key=str(uuid.uuid4()))
    db.add(key_entry)
    db.commit()
    db.refresh(key_entry)

    return {
        "data": {
            "patient_key": key_entry.key,
            "message": "Registration successful"
        }
    }
