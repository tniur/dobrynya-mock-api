from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import PatientKey
from app.db import crud
import base64

router = APIRouter()

@router.get("/getPatientDocumentDetails")
def get_patient_document_details(
    patient_key: str = Query(...),
    document_id: int = Query(...),
    db: Session = Depends(get_db)
):
    patient_key_entry = db.query(PatientKey).filter(PatientKey.key == patient_key).first()
    if not patient_key_entry:
        raise HTTPException(status_code=401, detail="Invalid patient_key")

    document = crud.get_patient_document_detail(db, patient_key_entry.patient_id, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        with open(document.pdf_path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="PDF file not found on server")

    result = {
        "title": document.title,
        "doctor_id": document.doctor_id,
        "clinic_id": document.clinic_id,
        "symptoms": document.symptoms,
        "diagnosis": document.diagnosis,
        "conclusion": document.conclusion,
        "recommendations": document.recommendations,
        "is_temp": document.is_temp,
        "date_return": document.date_return,
        "pdf_content": encoded_pdf
    }
    return {"data": result}
