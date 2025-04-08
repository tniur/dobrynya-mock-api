from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

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

user_clinics = Table(
    "user_clinics",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("clinic_id", Integer, ForeignKey("clinics.id"))
)

user_professions = Table(
    "user_professions",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("profession_id", Integer, ForeignKey("professions.id"))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    avatar = Column(String)
    avatar_small = Column(String)
    name = Column(String)
    birth_date = Column(String)
    gender = Column(String)
    phone = Column(String)
    email = Column(String)

    clinics = relationship("Clinic", secondary=user_clinics, backref="users")
    professions = relationship("Profession", secondary=user_professions, backref="users")