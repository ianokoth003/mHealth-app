import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

FLASK_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/healthease_db")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change_this_jwt_secret")
JWT_EXP_SECONDS = int(os.getenv("JWT_EXP_SECONDS", "86400"))  # 24 hours default
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")

# ---- Add MongoDB client here ----
mongo = MongoClient(MONGO_URI)
db = mongo.get_database()   # gets the default DB from URI
