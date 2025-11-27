"""
Simple DB verification script.
Connects to the MongoDB configured in environment (or default) and prints:
 - DB name
 - Collections
 - Number of documents in main collections
 - One sample document per collection

Run: python verify_db.py
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mhealth")

print(f"Connecting to MongoDB: {MONGO_URI}")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
except Exception as e:
    print("ERROR: Could not connect to MongoDB:\n", e)
    raise SystemExit(1)

db = client.get_database()
print(f"Using database: {db.name}\n")

cols = db.list_collection_names()
print("Collections:")
for c in cols:
    count = db[c].count_documents({})
    print(f" - {c}: {count} documents")

print("\nSample documents (up to 2 per collection):")
for c in cols:
    docs = list(db[c].find().limit(2))
    print(f"\nCollection: {c}")
    if not docs:
        print("  (no documents)")
    else:
        for d in docs:
            d_copy = d.copy()
            # convert ObjectId to str for readability
            if d_copy.get("_id"):
                d_copy["_id"] = str(d_copy["_id"])
            pprint(d_copy)

client.close()
print("\nDone.")
