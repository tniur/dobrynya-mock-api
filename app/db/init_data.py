import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import (
    Base, Clinic, Profession, User, Patient, PatientKey, PatientLabResult,
    Service, ServiceCategories, user_clinics, user_professions, user_services,
    service_service_categories, PatientLabResultDetail, PatientDocument
)

def load_data():
    engine = create_engine("sqlite:///./db.sqlite3", connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    with open("../data/clinics.json") as f:
        clinics = json.load(f)
        for item in clinics:
            db.add(Clinic(**item))

    with open("../data/professions.json") as f:
        professions = json.load(f)
        for item in professions:
            db.add(Profession(**item))

    with open("../data/users.json") as f:
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

    with open("../data/service_categories.json") as f:
        service_categories = json.load(f)
        for item in service_categories:
            db.add(ServiceCategories(**item))

    with open("../data/services.json") as f:
        services = json.load(f)
        for item in services:
            categories = item.pop("category_id", [])

            service = Service(**item)
            db.add(service)
            db.flush()

            for cid in categories:
                db.execute(service_service_categories.insert().values(service_id=service.id, category_id=cid))

    with open("../data/patients.json") as f:
        patients = json.load(f)
        for item in patients:
            db.add(Patient(**item))

    with open("../data/patient_keys.json") as f:
        keys = json.load(f)
        for item in keys:
            db.add(PatientKey(**item))

    with open("../data/lab_results.json") as f:
        lab_results = json.load(f)
        for item in lab_results:
            db.add(PatientLabResult(**item))

    with open("../data/patient_lab_result_details.json") as f:
        details = json.load(f)
        for item in details:
            db.add(PatientLabResultDetail(**item))

    with open("../data/patient_documents.json") as f:
        documents = json.load(f)
        for item in documents:
            db.add(PatientDocument(**item))

    db.commit()
    db.close()

if __name__ == "__main__":
    load_data()
