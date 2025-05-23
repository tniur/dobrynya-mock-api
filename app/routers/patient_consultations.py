from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey, User
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

    result = []
    for consult in consultations:
        doctor = db.query(User).filter_by(id=consult.doctor_id).first()
        doctor_name = doctor.name

        result.append({
            "id": consult.id,
            "title": consult.title,
            "doctor_id": consult.doctor_id,
            "doctor_name": doctor_name,
            "status": consult.status
        })

    return {"data": result}