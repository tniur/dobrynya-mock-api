from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey, User
from app.db import crud

router = APIRouter()

@router.get("/getPatientConsultationDetails")
def get_patient_consultation_details(
    patient_key: str = Query(...),
    consultation_id: int = Query(...),
    db: Session = Depends(get_db)
):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    consultation = crud.get_consultation_detail(db, patient_key_entry.patient_id, consultation_id)
    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    doctor = db.query(User).filter_by(id=consultation.doctor_id).first()
    doctor_name = doctor.name

    result = {
        "id": consultation.id,
        "title": consultation.title,
        "doctor_id": consultation.doctor_id,
        "doctor_name": doctor_name,
        "status": consultation.status,
        "desc": consultation.desc
    }
    return {"data": result}