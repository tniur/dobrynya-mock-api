from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import (
    clinics, professions, users, service_categories, services, patients, patient_lab_results,
    patients_lab_results_details, patient_documents, patient_document_details, patient_consultations,
    patient_consultation_details, patient_appointments, create_patient_appointments, cancel_patient_appointment,
    user_schedule, upload_avatar
)

app = FastAPI(title="Mock DobrynyaNN API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(clinics.router, tags=["Clinics"])
app.include_router(professions.router, tags=["Professions"])
app.include_router(users.router, tags=["Users"])
app.include_router(service_categories.router, tags=["ServiceCategories"])
app.include_router(services.router, tags=["Services"])
app.include_router(patients.router, tags=["Patients"])
app.include_router(patient_lab_results.router, tags=["Patient Lab Results"])
app.include_router(patients_lab_results_details.router, tags=["Patient Lab Results Details"])
app.include_router(patient_documents.router, tags=["Patient Documents"])
app.include_router(patient_document_details.router, tags=["Patient Document Details"])
app.include_router(patient_consultations.router, tags=["Patient Consultation"])
app.include_router(patient_consultation_details.router, tags=["Patient Consultation Details"])
app.include_router(patient_appointments.router, tags=["Patient Appointments"])
app.include_router(create_patient_appointments.router, tags=["Create Patient Appointments"])
app.include_router(cancel_patient_appointment.router, tags=["Cancel Patient Appointments"])
app.include_router(user_schedule.router, tags=["User Schedule"])
app.include_router(upload_avatar.router, tags=["Patient Avatar"])