from flask import current_app
from bson.objectid import ObjectId
from datetime import datetime

def get_appointments_collection():
    return current_app.mongo.db.appointments

def create_appointment(data):
    data_copy = data.copy()
    data_copy["created_at"] = datetime.utcnow()
    res = get_appointments_collection().insert_one(data_copy)
    return get_appointments_collection().find_one({"_id": res.inserted_id})

def list_appointments_for_patient(patient_id):
    return list(get_appointments_collection().find({"patient_id": patient_id}).sort("created_at", -1))

def list_appointments_for_doctor(doctor_id):
    return list(get_appointments_collection().find({"doctor_id": doctor_id}).sort("created_at", -1))
