from flask import current_app
from bson.objectid import ObjectId
from datetime import datetime

def get_records_collection():
    return current_app.mongo.db.records

def create_record(data):
    data_copy = data.copy()
    data_copy["created_at"] = datetime.utcnow()
    res = get_records_collection().insert_one(data_copy)
    return get_records_collection().find_one({"_id": res.inserted_id})

def get_patient_records(patient_id):
    return list(get_records_collection().find({"patient_id": patient_id}).sort("created_at", -1))

def get_record_by_id(rid):
    return get_records_collection().find_one({"_id": ObjectId(rid)})
