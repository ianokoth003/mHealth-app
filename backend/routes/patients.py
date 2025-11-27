# routes/patients.py
from flask import Blueprint, request, current_app, jsonify
from bson import ObjectId
import datetime
from utils.helpers import decode_jwt

patients_bp = Blueprint("patients", __name__)

def require_db():
    return current_app.db

def strid(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@patients_bp.route("/", methods=["POST"])
@patients_bp.route("", methods=["POST"])
def create_patient():
    db = require_db()
    data = request.json or {}
    # basic fields
    patient = {
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "dob": data.get("dob"),
        "sex": data.get("sex"),
        "address": data.get("address"),
        "contact": data.get("contact"),
        "clinical_id": data.get("clinical_id"), # optional unique id
        "allergies": data.get("allergies", ""),
        "history": data.get("history", ""),
        "created_at": datetime.datetime.utcnow(),
        "synced": True
    }
    res = db.patients.insert_one(patient)
    patient["_id"] = str(res.inserted_id)
    return jsonify(patient), 201

@patients_bp.route("/", methods=["GET"])
@patients_bp.route("", methods=["GET"])
def list_patients():
    db = require_db()
    q = {}
    name = request.args.get("q")
    if name:
        q["$or"] = [{"first_name": {"$regex": name, "$options":"i"}},{"last_name":{"$regex":name,"$options":"i"}}]

    # pagination
    try:
        page = max(1, int(request.args.get("page", 1)))
    except Exception:
        page = 1
    try:
        per_page = max(1, min(200, int(request.args.get("per_page", 20))))
    except Exception:
        per_page = 20

    skip = (page - 1) * per_page

    total = db.patients.count_documents(q)
    docs_cursor = db.patients.find(q).sort("created_at", -1).skip(skip).limit(per_page)
    docs = list(docs_cursor)
    out = [strid(d) for d in docs]
    total_pages = (total + per_page - 1) // per_page if per_page else 1

    return jsonify({
        "items": out,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages
        }
    })

@patients_bp.route("/<id>", methods=["GET"])
@patients_bp.route("/<id>/", methods=["GET"])
def get_patient(id):
    db = require_db()
    doc = db.patients.find_one({"_id": ObjectId(id)})
    if not doc: return jsonify({"error":"not found"}),404
    return jsonify(strid(doc))


@patients_bp.route("/<id>", methods=["PUT"])
@patients_bp.route("/<id>/", methods=["PUT"])
def update_patient(id):
    db = require_db()
    data = request.json or {}
    update_fields = {}
    for key in ("first_name","last_name","dob","sex","address","contact","clinical_id","allergies","history"):
        if key in data:
            update_fields[key] = data.get(key)
    if not update_fields:
        return jsonify({"error":"no fields to update"}), 400
    res = db.patients.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_fields}, return_document=True)
    if not res:
        return jsonify({"error":"not found"}), 404
    return jsonify(strid(res))


@patients_bp.route("/<id>", methods=["DELETE"])
@patients_bp.route("/<id>/", methods=["DELETE"])
def delete_patient(id):
    db = require_db()
    res = db.patients.delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        return jsonify({"error":"not found"}), 404
    return jsonify({"success": True}), 200
