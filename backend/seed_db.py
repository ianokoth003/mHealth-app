#!/usr/bin/env python
"""
Database seed script for mHealth application
This script adds sample data for testing
"""

import sys
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/mhealth")

def seed_database():
    """Seed database with sample data"""
    try:
        print(f"🔗 Connecting to MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        db = client.get_database()
        print(f"📦 Using database: {db.name}")
        
        # Clear existing data
        print("\n🗑️  Clearing existing data...")
        db.users.delete_many({})
        db.patients.delete_many({})
        db.appointments.delete_many({})
        db.records.delete_many({})
        
        # Seed users
        print("\n👥 Seeding users...")
        users = [
            {
                "email": "admin@mhealth.com",
                "password": generate_password_hash("admin123"),
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "created_at": datetime.utcnow()
            },
            {
                "email": "doctor@mhealth.com",
                "password": generate_password_hash("doctor123"),
                "first_name": "Dr.",
                "last_name": "Smith",
                "role": "doctor",
                "specialization": "General Practice",
                "created_at": datetime.utcnow()
            },
            {
                "email": "patient@mhealth.com",
                "password": generate_password_hash("patient123"),
                "first_name": "John",
                "last_name": "Doe",
                "role": "patient",
                "created_at": datetime.utcnow()
            }
        ]
        result = db.users.insert_many(users)
        print(f"✅ Inserted {len(result.inserted_ids)} users")
        
        # Seed patients
        print("\n🏥 Seeding patients...")
        patients = [
            {
                "first_name": "Alice",
                "last_name": "Johnson",
                "dob": "1990-05-15",
                "sex": "Female",
                "contact": "+1-555-0101",
                "address": "123 Main St, City, State",
                "allergies": "Penicillin",
                "history": "Asthma, seasonal allergies",
                "clinical_id": "CLIN001",
                "synced": True,
                "created_at": datetime.utcnow()
            },
            {
                "first_name": "Bob",
                "last_name": "Williams",
                "dob": "1985-08-22",
                "sex": "Male",
                "contact": "+1-555-0102",
                "address": "456 Oak Ave, City, State",
                "allergies": "None",
                "history": "Hypertension",
                "clinical_id": "CLIN002",
                "synced": True,
                "created_at": datetime.utcnow()
            },
            {
                "first_name": "Carol",
                "last_name": "Brown",
                "dob": "1995-12-08",
                "sex": "Female",
                "contact": "+1-555-0103",
                "address": "789 Pine Rd, City, State",
                "allergies": "Sulfa drugs",
                "history": "Migraine, anxiety",
                "clinical_id": "CLIN003",
                "synced": True,
                "created_at": datetime.utcnow()
            }
        ]
        result = db.patients.insert_many(patients)
        patient_ids = result.inserted_ids
        print(f"✅ Inserted {len(patient_ids)} patients")
        
        # Seed records
        print("\n📋 Seeding medical records...")
        records = [
            {
                "patient_id": str(patient_ids[0]),
                "doctor_id": str(result.inserted_ids[1]) if len(result.inserted_ids) > 1 else "doctor1",
                "type": "consultation",
                "title": "General Checkup",
                "notes": "Patient reports feeling well. Blood pressure normal.",
                "diagnosis": "No issues",
                "treatment": "Continue current medications",
                "created_at": datetime.utcnow()
            },
            {
                "patient_id": str(patient_ids[1]),
                "doctor_id": str(result.inserted_ids[1]) if len(result.inserted_ids) > 1 else "doctor1",
                "type": "lab_test",
                "title": "Blood Work",
                "notes": "Complete blood count performed",
                "results": "All values within normal range",
                "created_at": datetime.utcnow()
            }
        ]
        result = db.records.insert_many(records)
        print(f"✅ Inserted {len(result.inserted_ids)} records")
        
        # Seed appointments
        print("\n📅 Seeding appointments...")
        tomorrow = datetime.utcnow() + timedelta(days=1)
        appointments = [
            {
                "patient_id": str(patient_ids[0]),
                "doctor_id": "doctor1",
                "date": tomorrow.strftime("%Y-%m-%d"),
                "time": "10:00 AM",
                "status": "scheduled",
                "notes": "Follow-up consultation",
                "created_at": datetime.utcnow()
            },
            {
                "patient_id": str(patient_ids[1]),
                "doctor_id": "doctor1",
                "date": (tomorrow + timedelta(days=2)).strftime("%Y-%m-%d"),
                "time": "2:00 PM",
                "status": "scheduled",
                "notes": "Lab results review",
                "created_at": datetime.utcnow()
            }
        ]
        result = db.appointments.insert_many(appointments)
        print(f"✅ Inserted {len(result.inserted_ids)} appointments")
        
        print("\n" + "="*50)
        print("🎉 Database seeding complete!")
        print("="*50)
        print("\n📝 Test Credentials:")
        print("   Admin: admin@mhealth.com / admin123")
        print("   Doctor: doctor@mhealth.com / doctor123")
        print("   Patient: patient@mhealth.com / patient123")
        
        client.close()
        return True
        
    except ServerSelectionTimeoutError:
        print("❌ Error: Could not connect to MongoDB")
        print("   MongoDB is not running. Please start it first.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
