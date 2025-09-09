# backend/init_db.py
from app.database import engine, Base, SessionLocal
from app.models import Station, User
from app.utils.auth import get_password_hash

def init_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if stations exist
        if db.query(Station).count() == 0:
            # Add sample stations
            stations = [
                Station(
                    name="Central Station",
                    line="Red Line",
                    latitude=40.7128,
                    longitude=-74.0060,
                    station_type="metro"
                ),
                Station(
                    name="Downtown Station",
                    line="Blue Line",
                    latitude=40.7580,
                    longitude=-73.9855,
                    station_type="metro"
                ),
                Station(
                    name="Airport Station",
                    line="Green Line",
                    latitude=40.6413,
                    longitude=-73.7781,
                    station_type="train"
                ),
                Station(
                    name="University Station",
                    line="Red Line",
                    latitude=40.7295,
                    longitude=-73.9965,
                    station_type="metro"
                ),
                Station(
                    name="Business District",
                    line="Blue Line",
                    latitude=40.7614,
                    longitude=-73.9776,
                    station_type="metro"
                ),
                Station(
                    name="Park Avenue",
                    line="Green Line",
                    latitude=40.7489,
                    longitude=-73.9680,
                    station_type="bus"
                ),
                Station(
                    name="Harbor Station",
                    line="Yellow Line",
                    latitude=40.7074,
                    longitude=-74.0113,
                    station_type="metro"
                ),
                Station(
                    name="Stadium Station",
                    line="Red Line",
                    latitude=40.7505,
                    longitude=-73.9934,
                    station_type="metro"
                )
            ]
            
            for station in stations:
                db.add(station)
            
            db.commit()
            print("Sample stations added to database")
        
        # Check if demo user exists
        if db.query(User).filter(User.username == "demo").count() == 0:
            demo_user = User(
                email="demo@example.com",
                username="demo",
                hashed_password=get_password_hash("demo123")
            )
            db.add(demo_user)
            db.commit()
            print("Demo user created (username: demo, password: demo123)")
        
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()