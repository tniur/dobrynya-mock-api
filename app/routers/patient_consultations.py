from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from app.db import crud

router = APIRouter()

@router.get("/getPatientConsultations")
def get_patient_consultations(
    patient_key: str = Query(...),
    status: str | None = Query(None, regex="^(waiting|active|done)?$"),
    db: Session = Depends(get_db)
):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    consultations = crud.get_consultations_by_patient(db, patient_key_entry.patient_id, status)

    return [
        {
            "id": consult.id,
            "title": consult.title,
            "doctor_id": consult.doctor_id,
            "status": consult.status
        }
        for consult in consultations
    ]