from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from datetime import datetime

router = APIRouter()

def calculate_age(birth_date_str: str) -> int:
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

@router.get("/getPatientInfo")
def get_patient_info(patient_key: str = Query(...), db: Session = Depends(get_db)):
    key_entry = db.query(PatientKey).filter_by(key=patient_key).first()
    if not key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    patient = key_entry.patient

    avatar_path = f"/static/{patient.avatar_path}" if patient.avatar_path else None

    result = {
        "last_name": patient.last_name or None,
        "first_name": patient.first_name or None,
        "third_name": patient.third_name or None,
        "birth_date": patient.birth_date or None,
        "age": calculate_age(patient.birth_date) if patient.birth_date else None,
        "gender": patient.gender or None,
        "mobile": patient.mobile,
        "email": patient.email,
        "avatar_path": avatar_path or None,
    }
    return {"data": result}
