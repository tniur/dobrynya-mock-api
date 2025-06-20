from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Clinic(Base):
    __tablename__ = "clinics"
    id = Column(Integer, primary_key=True)
    title_ru = Column(String)
    title_en = Column(String)
    doctor_name_ru = Column(String)
    doctor_name_en = Column(String)
    real_address_ru = Column(String)
    real_address_en = Column(String)
    phone = Column(String)

class Profession(Base):
    __tablename__ = "professions"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    doctor_name = Column(String)

user_services = Table(
    "user_services",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("service_id", Integer, ForeignKey("services.id"))
)

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
    avatar_path = Column(String, nullable=True)
    avatar_small_path = Column(String, nullable=True)
    name = Column(String)
    birth_date = Column(String)
    gender = Column(String)
    phone = Column(String)
    email = Column(String)

    clinics = relationship("Clinic", secondary=user_clinics, backref="users")
    professions = relationship("Profession", secondary=user_professions, backref="users")
    services = relationship("Service", secondary=user_services, backref="users")

class ServiceCategories(Base):
    __tablename__ = "service_categories"
    id = Column(Integer, primary_key=True)
    title_ru = Column(String)
    title_en = Column(String)

service_service_categories = Table(
    "service_service_categories",
    Base.metadata,
    Column("service_id", Integer, ForeignKey("services.id")),
    Column("category_id", Integer, ForeignKey("service_categories.id"))
)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    duration = Column(Integer)
    profession_id = Column(Integer)
    short_desc = Column(String)
    full_desc = Column(String)

    category_ids = relationship("ServiceCategories", secondary=service_service_categories, backref="services")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True)
    last_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    third_name = Column(String, nullable=True)
    birth_date = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    mobile = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    avatar_path = Column(String, nullable=True)

class PatientKey(Base):
    __tablename__ = "patient_keys"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    key = Column(String, unique=True)

    patient = relationship("Patient", backref="keys")

class PatientLabResult(Base):
    __tablename__ = "patient_lab_results"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date_created = Column(String)
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(String)  # "normal", "abnormal", "in_progress"
    files_count = Column(Integer)

class PatientLabResultDetail(Base):
    __tablename__ = "patient_lab_result_details"
    id = Column(Integer, primary_key=True)
    result_id = Column(Integer, ForeignKey("patient_lab_results.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    status = Column(String)  # "normal", "abnormal", "in_progress"
    file_path = Column(String)

class PatientDocument(Base):
    __tablename__ = "patient_documents"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    title = Column(String)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    symptoms = Column(String)
    diagnosis = Column(String)
    conclusion = Column(String)
    recommendations = Column(String)
    is_temp = Column(Boolean, default=False)
    date_return = Column(String)
    pdf_path = Column(String)

class PatientConsultation(Base):
    __tablename__ = "patient_consultations"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    title = Column(String)
    doctor_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)  # "waiting", "active", "done"
    desc = Column(String)

class PatientAppointment(Base):
    __tablename__ = "patient_appointments"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(String)  # Формат: "2025-04-07"
    time = Column(String)  # Формат: "12:00 - 12:30"
    time_start = Column(String)  # Формат: "2025-04-07 12:00"
    time_end = Column(String)    # Формат: "2025-04-07 12:30"
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
    doctor_id = Column(Integer, ForeignKey("users.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    created = Column(String)  # Дата создания записи
    status = Column(String)   # "upcoming", "completed", "refused"

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    clinic_id = Column(Integer, ForeignKey('clinics.id'))
    date = Column(String)  # Формат: "2025-04-07"
    time = Column(String)  # Формат: "12:00 - 12:30"
    time_start = Column(String)  # Формат: "2025-04-07 12:00"
    time_end = Column(String)  # Формат: "2025-04-07 12:30"
    room = Column(String)
    is_busy = Column(Boolean, default=False)
