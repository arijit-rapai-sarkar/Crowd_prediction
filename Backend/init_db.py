# backend/init_db.py
import asyncio
from datetime import datetime, timedelta, timezone
import random
from app.database import get_sync_database
from app.utils.auth import get_password_hash
from bson import ObjectId
import os

def init_mongodb():
    """Initialize MongoDB with collections and sample data"""
    db = get_sync_database()
    
    if db is None:
        print("Error: Could not connect to MongoDB")
        return
    
    try:
        # Create indexes for better performance
        db.users.create_index([("email", 1)], unique=True)
        db.users.create_index([("username", 1)], unique=True)
        db.stations.create_index([("name", 1), ("line", 1)])
        db.crowd_reports.create_index([("station_id", 1), ("created_at", -1)])
        db.predictions.create_index([("station_id", 1), ("prediction_time", -1)])
        
        print("MongoDB indexes created successfully")

        # Safe password (truncate if needed to avoid bcrypt > 72-byte limit)
        default_password = os.getenv("DEFAULT_PASSWORD", "demo123")[:72]

        # Helper to get UTC datetime (fixes deprecation warning)
        def utc_now():
            return datetime.now(timezone.utc)

        # Check if stations exist
        if db.stations.count_documents({}) == 0:
            stations = [
                {"name": "Central Station", "line": "Red Line", "latitude": 40.7128, "longitude": -74.0060,
                 "station_type": "metro", "created_at": utc_now()},
                {"name": "Downtown Station", "line": "Blue Line", "latitude": 40.7580, "longitude": -73.9855,
                 "station_type": "metro", "created_at": utc_now()},
                {"name": "Airport Station", "line": "Green Line", "latitude": 40.6413, "longitude": -73.7781,
                 "station_type": "train", "created_at": utc_now()},
                {"name": "University Station", "line": "Red Line", "latitude": 40.7295, "longitude": -73.9965,
                 "station_type": "metro", "created_at": utc_now()},
                {"name": "Business District", "line": "Blue Line", "latitude": 40.7614, "longitude": -73.9776,
                 "station_type": "metro", "created_at": utc_now()},
                {"name": "Park Avenue", "line": "Green Line", "latitude": 40.7489, "longitude": -73.9680,
                 "station_type": "bus", "created_at": utc_now()},
                {"name": "Harbor Station", "line": "Yellow Line", "latitude": 40.7074, "longitude": -74.0113,
                 "station_type": "metro", "created_at": utc_now()},
                {"name": "Stadium Station", "line": "Red Line", "latitude": 40.7505, "longitude": -73.9934,
                 "station_type": "metro", "created_at": utc_now()},
            ]
            
            result = db.stations.insert_many(stations)
            print(f"Sample stations added to database: {len(result.inserted_ids)} stations")
            station_ids = [str(id) for id in result.inserted_ids]
            
            # Create demo user
            demo_user_id = None
            if db.users.count_documents({"username": "demo"}) == 0:
                demo_user = {
                    "email": "demo@example.com",
                    "username": "demo",
                    "hashed_password": get_password_hash(default_password),
                    "is_active": True,
                    "created_at": utc_now()
                }
                demo_result = db.users.insert_one(demo_user)
                demo_user_id = str(demo_result.inserted_id)
                print(f"Demo user created (username: demo, password: {default_password})")
            else:
                demo_user = db.users.find_one({"username": "demo"})
                if demo_user:
                    demo_user_id = str(demo_user["_id"])
            
            # Generate sample crowd reports for the last 30 days
            crowd_reports = []
            for days_ago in range(30):
                report_date = utc_now() - timedelta(days=days_ago)
                for hour in [8, 12, 17, 20]:
                    report_time = report_date.replace(hour=hour, minute=random.randint(0, 59))
                    for station_id in station_ids:
                        if random.random() < 0.3:
                            continue
                        base_crowd = 4.0 if hour in [8, 17] else (3.0 if hour in [12, 20] else 2.5)
                        crowd_level = max(1, min(5, int(base_crowd + random.uniform(-1, 1))))
                        crowd_reports.append({
                            "station_id": station_id,
                            "user_id": demo_user_id,
                            "crowd_level": crowd_level,
                            "description": f"Sample crowd report for level {crowd_level}",
                            "created_at": report_time
                        })
            if crowd_reports:
                db.crowd_reports.insert_many(crowd_reports)
                print(f"Sample crowd reports added: {len(crowd_reports)} reports")

        # Ensure demo user exists even if stations already existed
        if db.users.count_documents({"username": "demo"}) == 0:
            demo_user = {
                "email": "demo@example.com",
                "username": "demo",
                "hashed_password": get_password_hash(default_password),
                "is_active": True,
                "created_at": utc_now()
            }
            db.users.insert_one(demo_user)
            print(f"Demo user created (username: demo, password: {default_password})")
        
        print("MongoDB initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_mongodb()
