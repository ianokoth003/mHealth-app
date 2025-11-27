from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.record_model import create_record, get_patient_records, get_record_by_id
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename

records_bp = Blueprint("records", __name__)

ALLOWED_EXT = {"png", "jpg", "jpeg", "pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@records_bp.route("/create", methods=["POST"])
@jwt_required()
def create():
    # Accept JSON or form-data with optional file
    data = request.form.to_dict() if request.form else request.get_json() or {}
    if "patient_id" not in data:
        return jsonify({"error": "patient_id required"}), 400
    # file handling
    if "file" in request.files:
        f = request.files["file"]
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            f.save(filepath)
            data["file_path"] = filepath
    rec = create_record(data)
    rec["_id"] = str(rec["_id"])
    return jsonify({"record": rec}), 201

@records_bp.route("/patient/<patient_id>", methods=["GET"])
@jwt_required()
def list_patient(patient_id):
    records = get_patient_records(patient_id)
    for r in records:
        r["_id"] = str(r["_id"])
    return jsonify({"records": records})

@records_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename, as_attachment=True)
