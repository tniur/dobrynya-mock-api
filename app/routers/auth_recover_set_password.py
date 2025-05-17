from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Patient, PatientKey
import uuid

router = APIRouter()

@router.post("/auth/recover/setPassword")
def recover_set_password(
    email: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.email == email).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient.password = new_password
    db.add(patient)

    key_entry = db.query(PatientKey).filter(PatientKey.patient_id == patient.id).first()
    if not key_entry:
        key_entry = PatientKey(patient_id=patient.id, key=str(uuid.uuid4()))
        db.add(key_entry)

    db.commit()
    db.refresh(key_entry)

    return {
        "data": {
            "patient_key": key_entry.key,
            "message": "Login successful"
        }
    }
