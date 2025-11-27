from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

def create_tokens(identity, expires_delta_minutes=60*24):
    access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=expires_delta_minutes))
    return {"access_token": access_token}
