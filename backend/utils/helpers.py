# utils/helpers.py
from passlib.hash import bcrypt
import jwt
import config
from datetime import datetime, timedelta

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(password, hashed):
    return bcrypt.verify(password, hashed)

def create_jwt(payload):
    exp = datetime.utcnow() + timedelta(seconds=config.JWT_EXP_SECONDS)
    token = jwt.encode({**payload, "exp": exp}, config.SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt(token):
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None
