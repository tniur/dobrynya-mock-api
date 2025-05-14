from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey, Service
from app.db import crud

router = APIRouter()

@router.get("/getPatientLabResults")
def get_patient_lab_results(patient_key: str = Query(...), db: Session = Depends(get_db)):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    lab_results = crud.get_lab_results_by_patient(db, patient_key_entry.patient_id)

    result = []
    for lab_result in lab_results:
        service = db.query(Service).filter_by(id=lab_result.service_id).first()
        service_name = service.title

        result.append({
            "result_id": lab_result.id,
            "files_count": lab_result.files_count,
            "date_created": lab_result.date_created,
            "clinic_id": lab_result.clinic_id,
            "service_id": lab_result.service_id,
            "service_name": service_name,
            "status": lab_result.status
        })
    return {"data": result}
