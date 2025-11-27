#!/usr/bin/env python
"""
Database initialization script for mHealth application
This script creates collections and indexes in MongoDB
"""

import sys
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mhealth")

def init_database():
    """Initialize MongoDB database with collections and indexes"""
    try:
        print(f"🔗 Connecting to MongoDB: {MONGO_URI}")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        db = client.get_database()
        print(f"📦 Using database: {db.name}")
        
        # Create collections
        collections = ["users", "patients", "appointments", "records", "consultations"]
        
        for collection_name in collections:
            if collection_name not in db.list_collection_names():
                db.create_collection(collection_name)
                print(f"✅ Created collection: {collection_name}")
            else:
                print(f"ℹ️  Collection already exists: {collection_name}")
        
        # Create indexes
        print("\n📊 Creating indexes...")
        
        # Users indexes
        db.users.create_index([("email", 1)], unique=True, sparse=True)
        print("✅ Created index: users.email")
        
        db.users.create_index([("created_at", -1)])
        print("✅ Created index: users.created_at")
        
        # Patients indexes
        db.patients.create_index([("first_name", 1), ("last_name", 1)])
        print("✅ Created index: patients.name")
        
        db.patients.create_index([("contact", 1)], sparse=True)
        print("✅ Created index: patients.contact")
        
        db.patients.create_index([("created_at", -1)])
        print("✅ Created index: patients.created_at")
        
        # Appointments indexes
        db.appointments.create_index([("patient_id", 1)])
        print("✅ Created index: appointments.patient_id")
        
        db.appointments.create_index([("doctor_id", 1)])
        print("✅ Created index: appointments.doctor_id")
        
        db.appointments.create_index([("created_at", -1)])
        print("✅ Created index: appointments.created_at")
        
        # Records indexes
        db.records.create_index([("patient_id", 1)])
        print("✅ Created index: records.patient_id")
        
        db.records.create_index([("created_at", -1)])
        print("✅ Created index: records.created_at")
        
        # Consultations indexes
        db.consultations.create_index([("patient_id", 1)])
        print("✅ Created index: consultations.patient_id")
        
        db.consultations.create_index([("doctor_id", 1)])
        print("✅ Created index: consultations.doctor_id")
        
        print("\n" + "="*50)
        print("🎉 Database initialization complete!")
        print("="*50)
        
        # Show database stats
        stats = db.command("dbstats")
        print(f"\nDatabase: {stats['db']}")
        print(f"Collections: {stats['collections']}")
        print(f"Data size: {stats['dataSize']} bytes")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ Error: Could not connect to MongoDB")
        print(f"   Connection string: {MONGO_URI}")
        print("\n   MongoDB is not running. Please:")
        print("   1. Install MongoDB from: https://www.mongodb.com/try/download/community")
        print("   2. Start MongoDB service (usually runs automatically)")
        print("   3. Or use MongoDB Atlas cloud: https://www.mongodb.com/cloud/atlas")
        print("   4. Or run Docker: docker run -d -p 27017:27017 --name mongodb mongo:latest")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
