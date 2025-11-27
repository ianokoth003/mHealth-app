from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

def get_users_collection():
    return current_app.mongo.db.users

def create_user(payload: dict):
    users = get_users_collection()
    payload_copy = payload.copy()
    payload_copy["password"] = generate_password_hash(payload_copy["password"])
    users.insert_one(payload_copy)
    return payload_copy

def find_by_email(email: str):
    users = get_users_collection()
    return users.find_one({"email": email})

def verify_password(hashed_pw, password_plain):
    return check_password_hash(hashed_pw, password_plain)

def find_by_id(uid):
    users = get_users_collection()
    from bson.objectid import ObjectId
    return users.find_one({"_id": ObjectId(uid)})
