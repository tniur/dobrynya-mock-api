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

    avatar_path = None
    if patient.avatar_path:
        avatar_path = f"/static/{patient.avatar_path}"

    result = {
        "last_name": patient.last_name,
        "first_name": patient.first_name,
        "third_name": patient.third_name,
        "birth_date": patient.birth_date,
        "age": calculate_age(patient.birth_date),
        "gender": patient.gender,
        "mobile": patient.mobile,
        "email": patient.email,
        "avatar_path": avatar_path,
    }
    return {"data": result}
