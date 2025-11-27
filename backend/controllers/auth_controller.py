from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from config import mongo

auth_bp = Blueprint("auth", __name__)

# =============== REGISTER ===============
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["name", "email", "password"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    user_exist = mongo.db.users.find_one({"email": data["email"]})
    if user_exist:
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(data["password"])
    new_user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
    }

    mongo.db.users.insert_one(new_user)
    return jsonify({"message": "User registered successfully"}), 201


# =============== LOGIN ===============
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    user = mongo.db.users.find_one({"email": data.get("email")})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], data.get("password", "")):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }), 200
