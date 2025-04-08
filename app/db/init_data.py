import json
from app.db.models import Base, Clinic, Profession, User, user_clinics, user_professions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

            user = User(**item)
            db.add(user)
            db.flush()

            for pid in professions:
                db.execute(user_professions.insert().values(user_id=user.id, profession_id=pid))
            for cid in clinics:
                db.execute(user_clinics.insert().values(user_id=user.id, clinic_id=cid))

    db.commit()
    db.close()

if __name__ == "__main__":
    load_data()
