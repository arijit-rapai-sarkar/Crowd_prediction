# backend/init_db.py
import asyncio
from datetime import datetime, timedelta
import random
from app.database import get_sync_database
from app.utils.auth import get_password_hash
from bson import ObjectId

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
        
        # Check if stations exist
        if db.stations.count_documents({}) == 0:
            # Add sample stations
            stations = [
                {
                    "name": "Central Station",
                    "line": "Red Line",
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "station_type": "metro",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Downtown Station",
                    "line": "Blue Line",
                    "latitude": 40.7580,
                    "longitude": -73.9855,
                    "station_type": "metro",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Airport Station",
                    "line": "Green Line",
                    "latitude": 40.6413,
                    "longitude": -73.7781,
                    "station_type": "train",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "University Station",
                    "line": "Red Line",
                    "latitude": 40.7295,
                    "longitude": -73.9965,
                    "station_type": "metro",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Business District",
                    "line": "Blue Line",
                    "latitude": 40.7614,
                    "longitude": -73.9776,
                    "station_type": "metro",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Park Avenue",
                    "line": "Green Line",
                    "latitude": 40.7489,
                    "longitude": -73.9680,
                    "station_type": "bus",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Harbor Station",
                    "line": "Yellow Line",
                    "latitude": 40.7074,
                    "longitude": -74.0113,
                    "station_type": "metro",
                    "created_at": datetime.utcnow()
                },
                {
                    "name": "Stadium Station",
                    "line": "Red Line",
                    "latitude": 40.7505,
                    "longitude": -73.9934,
                    "station_type": "metro",
                    "created_at": datetime.utcnow()
                }
            ]
            
            result = db.stations.insert_many(stations)
            print(f"Sample stations added to database: {len(result.inserted_ids)} stations")
            
            # Add sample crowd reports for demonstration
            station_ids = [str(id) for id in result.inserted_ids]
            
            # Create demo user first
            demo_user_id = None
            if db.users.count_documents({"username": "demo"}) == 0:
                demo_user = {
                    "email": "demo@example.com",
                    "username": "demo",
                    "hashed_password": get_password_hash("demo123"),
                    "is_active": True,
                    "created_at": datetime.utcnow()
                }
                demo_result = db.users.insert_one(demo_user)
                demo_user_id = str(demo_result.inserted_id)
                print("Demo user created (username: demo, password: demo123)")
            else:
                demo_user = db.users.find_one({"username": "demo"})
                if demo_user:
                    demo_user_id = str(demo_user["_id"])
            
            # Generate sample crowd reports over the last 30 days
            crowd_reports = []
            for days_ago in range(30):
                report_date = datetime.utcnow() - timedelta(days=days_ago)
                
                # Generate multiple reports per day for different hours
                for hour in [8, 12, 17, 20]:  # Peak times
                    report_time = report_date.replace(hour=hour, minute=random.randint(0, 59))
                    
                    for station_id in station_ids:
                        # Skip some reports randomly to simulate real data
                        if random.random() < 0.3:
                            continue
                        
                        # Generate crowd level based on time patterns
                        base_crowd = 2.5
                        if hour in [8, 17]:  # Rush hours
                            base_crowd = 4.0
                        elif hour in [12, 20]:  # Lunch/dinner
                            base_crowd = 3.0
                        
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
        
        # Check if demo user exists (if stations already existed)
        if db.users.count_documents({"username": "demo"}) == 0:
            demo_user = {
                "email": "demo@example.com",
                "username": "demo",
                "hashed_password": get_password_hash("demo123"),
                "is_active": True,
                "created_at": datetime.utcnow()
            }
            db.users.insert_one(demo_user)
            print("Demo user created (username: demo, password: demo123)")
        
        print("MongoDB initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    init_mongodb()