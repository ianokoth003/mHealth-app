# routes/sync.py
from flask import Blueprint, request, current_app, jsonify
import datetime
from bson import ObjectId

sync_bp = Blueprint("sync", __name__)

@sync_bp.route("/upload", methods=["POST"])
def upload():
    """
    Expect payload: { records: [ {type: 'patient'|'consult', data: {...}} ] }
    Server stores them and returns ids mapping.
    """
    db = current_app.db
    payload = request.json or {}
    recs = payload.get("records", [])
    result_map = []
    for r in recs:
        typ = r.get("type")
        data = r.get("data", {})
        data["synced"] = True
        data["created_at"] = datetime.datetime.utcnow()
        if typ == "patient":
            res = db.patients.insert_one(data)
            result_map.append({"local_id": r.get("local_id"), "server_id": str(res.inserted_id), "type": "patient"})
        elif typ in ("consultation","consult"):
            res = db.consultations.insert_one(data)
            result_map.append({"local_id": r.get("local_id"), "server_id": str(res.inserted_id), "type":"consultation"})
    return jsonify({"uploaded": result_map})

@sync_bp.route("/download", methods=["GET"])
def download():
    """
    Client asks for changes since timestamp param: since=ISO or epoch
    We'll return latest patients and consultations (simple implementation)
    """
    db = current_app.db
    since = request.args.get("since")
    # simple - return all for now
    patients = list(db.patients.find().sort("created_at",-1).limit(1000))
    consults = list(db.consultations.find().sort("created_at",-1).limit(2000))
    def s(d): d["_id"] = str(d["_id"]); return d
    return jsonify({"patients":[s(p) for p in patients], "consultations":[s(c) for c in consults]})
