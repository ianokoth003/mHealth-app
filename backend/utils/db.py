from flask_pymongo import PyMongo
import os

mongo = PyMongo()

def init_db(app):
    # prefer MONGO_URI from environment/app config if present
    default_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/mhealth")
    if not app.config.get("MONGO_URI"):
        app.config["MONGO_URI"] = default_uri

    mongo.init_app(app)
    # expose mongo client and db on the Flask app for convenience
    app.mongo = mongo
    try:
        # PyMongo exposes the database via .db after init
        app.db = mongo.db
    except Exception:
        app.db = None
