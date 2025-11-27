from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.appointment_model import create_appointment, list_appointments_for_patient, list_appointments_for_doctor

appointments_bp = Blueprint("appointments", __name__)

@appointments_bp.route("/book", methods=["POST"])
@jwt_required()
def book():
    data = request.get_json() or {}
    required = ["patient_id", "doctor_id", "scheduled_time", "reason"]
    if not all(k in data for k in required):
        return jsonify({"error": f"required fields: {required}"}), 400
    appt = create_appointment(data)
    appt["_id"] = str(appt["_id"])
    return jsonify({"appointment": appt}), 201

@appointments_bp.route("/patient/<patient_id>", methods=["GET"])
@jwt_required()
def for_patient(patient_id):
    appts = list_appointments_for_patient(patient_id)
    for a in appts:
        a["_id"] = str(a["_id"])
    return jsonify({"appointments": appts})

@appointments_bp.route("/doctor/<doctor_id>", methods=["GET"])
@jwt_required()
def for_doctor(doctor_id):
    appts = list_appointments_for_doctor(doctor_id)
    for a in appts:
        a["_id"] = str(a["_id"])
    return jsonify({"appointments": appts})
