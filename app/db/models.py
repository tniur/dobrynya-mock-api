from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Clinic(Base):
    __tablename__ = "clinics"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    doctor_name = Column(String)
    real_address = Column(String)
    phone = Column(String)

class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    doctor_name = Column(String)
    is_deleted = Column(Boolean, default=False)
