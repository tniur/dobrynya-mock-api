from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from app.db import crud

router = APIRouter()

@router.get("/getPatientDocuments")
def get_patient_documents(patient_key: str = Query(...), db: Session = Depends(get_db)):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    documents = crud.get_patient_documents(db, patient_key_entry.patient_id)

    result = [
        {
            "id": doc.id,
            "title": doc.title,
            "doctor_id": doc.doctor_id,
            "symptoms": doc.symptoms,
            "diagnosis": doc.diagnosis,
            "conclusion": doc.conclusion,
            "recommendations": doc.recommendations,
            "is_temp": doc.is_temp,
            "date_return": doc.date_return
        }
        for doc in documents
    ]
    return {"data": result}
