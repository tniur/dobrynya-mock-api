from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from app.db import crud

router = APIRouter()

@router.get("/getPatientLabResults")
def get_patient_lab_results(patient_key: str = Query(...), db: Session = Depends(get_db)):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    lab_results = crud.get_lab_results_by_patient(db, patient_key_entry.patient_id)

    result = [
        {
            "result_id": result.id,
            "files_count": result.files_count,
            "date_created": result.date_created,
            "clinic_id": result.clinic_id
        }
        for result in lab_results
    ]
    return {"data": result}
