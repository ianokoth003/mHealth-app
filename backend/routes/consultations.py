# routes/consultations.py
from flask import Blueprint, request, current_app, jsonify
from bson import ObjectId
import datetime

consult_bp = Blueprint("consultations", __name__)

@consult_bp.route("/", methods=["POST"])
def create_consultation():
    db = current_app.db
    data = request.json or {}
    # expected fields: patient_id, provider_id, symptoms, diagnosis, vitals, prescriptions
    rec = {
        "patient_id": data.get("patient_id"),
        "provider_id": data.get("provider_id"),
        "symptoms": data.get("symptoms"),
        "diagnosis": data.get("diagnosis"),
        "vitals": data.get("vitals", {}),
        "prescriptions": data.get("prescriptions", []),
        "notes": data.get("notes",""),
        "created_at": datetime.datetime.utcnow(),
        "synced": True
    }
    res = db.consultations.insert_one(rec)
    rec["_id"] = str(res.inserted_id)
    return jsonify(rec),201

@consult_bp.route("/", methods=["GET"])
def list_consultations():
    db = current_app.db
    patient = request.args.get("patient_id")
    q = {}
    if patient: q["patient_id"] = patient
    docs = list(db.consultations.find(q).sort("created_at",-1).limit(300))
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs)
