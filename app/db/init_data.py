import json
from app.db.models import Base, Clinic, Profession
from app.db.database import engine, SessionLocal

def load_data():
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

    db.commit()
    db.close()

if __name__ == "__main__":
    load_data()
