from typing import List, Optional
from sqlalchemy.orm import Session
from .models import (Clinic, Profession, User, ServiceCategories, Service, PatientLabResult, PatientDocument,
                     PatientConsultation, PatientAppointment)

def get_all_clinics(db: Session):
    return db.query(Clinic).all()

def get_all_professions(db: Session):
    return db.query(Profession).all()

def get_filtered_users(
    db: Session,
    user_ids: Optional[List[int]] = None,
    clinic_id: Optional[int] = None,
    profession_id: Optional[int] = None,
    service_ids: Optional[List[int]] = None,
):
    query = db.query(User)

    if user_ids:
        query = query.filter(User.id.in_(user_ids))
    if clinic_id:
        query = query.filter(User.clinics.any(Clinic.id == clinic_id))
    if profession_id:
        query = query.filter(User.professions.any(Profession.id == profession_id))
    if service_ids:
        query = query.join(User.services).filter(Service.id.in_(service_ids))

    return query.all()

def get_all_service_categories(db: Session):
    return db.query(ServiceCategories).all()

def get_filtered_services(
    db: Session,
    service_ids: Optional[List[int]] = None,
    profession_id: Optional[int] = None,
    category_ids: Optional[List[int]] = None,
):
    query = db.query(Service)

    if service_ids:
        query = query.filter(Service.id.in_(service_ids))
    if profession_id:
        query = query.filter(Service.profession_id == profession_id)
    if category_ids:
        query = query.join(Service.category_ids).filter(ServiceCategories.id.in_(category_ids))

    return query.all()

def get_lab_results_by_patient(db: Session, patient_id: int):
    return db.query(PatientLabResult).filter(PatientLabResult.patient_id == patient_id).all()

def get_patient_documents(db: Session, patient_id: int):
    return db.query(PatientDocument).filter(PatientDocument.patient_id == patient_id).all()

def get_patient_document_detail(db: Session, patient_id: int, document_id: int):
    return db.query(PatientDocument).filter(
        PatientDocument.patient_id == patient_id,
        PatientDocument.id == document_id
    ).first()

def get_consultations_by_patient(db: Session, patient_id: int, status: str | None = None):
    query = db.query(PatientConsultation).filter(PatientConsultation.patient_id == patient_id)
    if status:
        query = query.filter(PatientConsultation.status == status)
    return query.all()

def get_consultation_detail(db: Session, patient_id: int, consultation_id: int):
    return db.query(PatientConsultation).filter(
        PatientConsultation.id == consultation_id,
        PatientConsultation.patient_id == patient_id
    ).first()

def get_appointments_by_patient(db: Session, patient_id: int):
    return db.query(PatientAppointment).filter(PatientAppointment.patient_id == patient_id).all()

def post_create_appointment(
    db: Session,
    patient_id: int,
    doctor_id: int,
    clinic_id: int,
    date: str,
    time: str,
    time_start: str,
    time_end: str,
    created: str,
    status: str = "upcoming"
):
    new_appointment = PatientAppointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        clinic_id=clinic_id,
        date=date,
        time=time,
        time_start=time_start,
        time_end=time_end,
        created=created,
        status=status
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

def cancel_appointment(db: Session, appointment_id: int):
    appointment = db.query(PatientAppointment).filter(PatientAppointment.id == appointment_id).first()
    if not appointment:
        raise ValueError("Appointment not found")

    appointment.status = "refused"

    db.commit()
    db.refresh(appointment)
    return appointment
