# routes/auth.py
from flask import Blueprint, request, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
import datetime
import jwt
import os

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "change_me")

def create_jwt(data):
    """Create a JWT token"""
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "worker")

    if not all([name, email, password]):
        return jsonify({"error": "name, email, password required"}), 400

    db = current_app.db
    if db.users.find_one({"email": email}):
        return jsonify({"error": "User exists"}), 400

    user = {
        "name": name,
        "email": email,
        "password": generate_password_hash(password),
        "role": role,
        "created_at": datetime.datetime.utcnow()
    }
    res = db.users.insert_one(user)
    user["_id"] = str(res.inserted_id)
    return jsonify({"message": "registered", "user": {"id": user["_id"], "name": name, "email": email}}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    if not all([email, password]):
        return jsonify({"error": "email, password required"}), 400

    db = current_app.db
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if not verify_password(password, user["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_jwt({"user_id": str(user["_id"]), "role": user.get("role", "worker")})
    user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip() or user.get("name", "User")
    return jsonify({"access_token": token, "user": {"id": str(user["_id"]), "name": user_name, "role": user.get("role")}}), 200
