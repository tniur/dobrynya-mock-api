from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
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

    return {
        "id": consultation.id,
        "title": consultation.title,
        "doctor_id": consultation.doctor_id,
        "status": consultation.status,
        "desc": consultation.desc
    }