import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from app.db.models import (
    Base, Clinic, Profession, User, Patient, PatientKey, PatientLabResult,
    Service, ServiceCategories, user_clinics, user_professions, user_services,
    service_service_categories, PatientLabResultDetail, PatientDocument,
    PatientConsultation, PatientAppointment, Schedule
)

def load_data():
    engine = create_engine("sqlite:///./app/db/db.sqlite3", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    clinics_path = Path(__file__).parent / 'data' / 'clinics.json'
    professions_path = Path(__file__).parent / 'data' / 'professions.json'
    users_path = Path(__file__).parent / 'data' / 'users.json'
    service_categories_path = Path(__file__).parent / 'data' / 'service_categories.json'
    services_path = Path(__file__).parent / 'data' / 'services.json'
    patients_path = Path(__file__).parent / 'data' / 'patients.json'
    patient_keys_path = Path(__file__).parent / 'data' / 'patient_keys.json'
    lab_results_path = Path(__file__).parent / 'data' / 'lab_results.json'
    patient_lab_result_details_path = Path(__file__).parent / 'data' / 'patient_lab_result_details.json'
    patient_documents_path = Path(__file__).parent / 'data' / 'patient_documents.json'
    patient_consultations_path = Path(__file__).parent / 'data' / 'patient_consultations.json'
    patient_appointments_path = Path(__file__).parent / 'data' / 'patient_appointments.json'
    schedules_path = Path(__file__).parent / 'data' / 'schedules.json'

    with open(clinics_path) as f:
        clinics = json.load(f)
        for item in clinics:
            db.add(Clinic(**item))

    with open(professions_path) as f:
        professions = json.load(f)
        for item in professions:
            db.add(Profession(**item))

    with open(users_path) as f:
        users = json.load(f)
        for item in users:
            professions = item.pop("profession", [])
            clinics = item.pop("clinic", [])
            services = item.pop("service", [])

            user = User(**item)
            db.add(user)
            db.flush()

            for pid in professions:
                db.execute(user_professions.insert().values(user_id=user.id, profession_id=pid))
            for cid in clinics:
                db.execute(user_clinics.insert().values(user_id=user.id, clinic_id=cid))
            for sid in services:
                db.execute(user_services.insert().values(user_id=user.id, service_id=sid))

    with open(service_categories_path) as f:
        service_categories = json.load(f)
        for item in service_categories:
            db.add(ServiceCategories(**item))

    with open(services_path) as f:
        services = json.load(f)
        for item in services:
            categories = item.pop("category_id", [])

            service = Service(**item)
            db.add(service)
            db.flush()

            for cid in categories:
                db.execute(service_service_categories.insert().values(service_id=service.id, category_id=cid))

    with open(patients_path) as f:
        patients = json.load(f)
        for item in patients:
            db.add(Patient(**item))

    with open(patient_keys_path) as f:
        keys = json.load(f)
        for item in keys:
            db.add(PatientKey(**item))

    with open(lab_results_path) as f:
        lab_results = json.load(f)
        for item in lab_results:
            db.add(PatientLabResult(**item))

    with open(patient_lab_result_details_path) as f:
        details = json.load(f)
        for item in details:
            db.add(PatientLabResultDetail(**item))

    with open(patient_documents_path) as f:
        documents = json.load(f)
        for item in documents:
            db.add(PatientDocument(**item))

    with open(patient_consultations_path) as f:
        consultations = json.load(f)
        for item in consultations:
            db.add(PatientConsultation(**item))

    with open(patient_appointments_path) as f:
        appointments = json.load(f)
        for item in appointments:
            db.add(PatientAppointment(**item))

    with open(schedules_path) as f:
        schedules = json.load(f)
        for item in schedules:
            db.add(Schedule(**item))

    db.commit()
    db.close()

if __name__ == "__main__":
    load_data()
