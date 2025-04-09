import base64
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey, PatientLabResult, PatientLabResultDetail

router = APIRouter()

@router.get("/getPatientLabResultDetails")
def get_lab_result_details(patient_key: str, result_id: int, db: Session = Depends(get_db)):
    patient = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    result = db.query(PatientLabResult).filter(
        PatientLabResult.id == result_id,
        PatientLabResult.patient_id == patient.patient_id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    files = db.query(PatientLabResultDetail).filter(
        PatientLabResultDetail.result_id == result.id
    ).all()

    pdf_files = []
    for file in files:
        try:
            with open(file.file_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                pdf_files.append(encoded)
        except FileNotFoundError:
            continue

    return {
        "date_created": result.date_created,
        "clinic_id": result.clinic_id,
        "pdf_files": pdf_files
    }
