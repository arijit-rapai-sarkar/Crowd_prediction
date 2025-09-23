from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from ..database import get_database
from ..models.station import Station
from ..models.crowd_report import CrowdReport
from ..schemas.station import StationCreate, StationResponse
from ..utils.dependencies import get_current_user
from datetime import datetime, timedelta
import pymongo

router = APIRouter(prefix="/api/stations", tags=["stations"])

@router.get("/", response_model=List[StationResponse])
async def get_stations(
    skip: int = 0,
    limit: int = 100
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Get stations from MongoDB
    cursor = db.stations.find().skip(skip).limit(limit)
    stations = await cursor.to_list(length=limit)
    
    # Add current crowd level for each station
    result = []
    for station in stations:
        # Get average crowd level from last hour
        last_hour = datetime.utcnow() - timedelta(hours=1)
        pipeline = [
            {
                "$match": {
                    "station_id": str(station["_id"]),
                    "created_at": {"$gte": last_hour}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "avg_crowd": {"$avg": "$crowd_level"}
                }
            }
        ]
        
        crowd_result = await db.crowd_reports.aggregate(pipeline).to_list(1)
        avg_crowd = crowd_result[0]["avg_crowd"] if crowd_result else None
        
        station_dict = {
            "id": str(station["_id"]),
            "name": station["name"],
            "line": station["line"],
            "latitude": station["latitude"],
            "longitude": station["longitude"],
            "station_type": station["station_type"],
            "created_at": station["created_at"],
            "current_crowd_level": round(float(avg_crowd), 2) if avg_crowd else None
        }
        result.append(station_dict)
    
    return result

@router.get("/{station_id}", response_model=StationResponse)
async def get_station(station_id: str):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Validate ObjectId
    try:
        obj_id = ObjectId(station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    station = await db.stations.find_one({"_id": obj_id})
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Get current crowd level
    last_hour = datetime.utcnow() - timedelta(hours=1)
    pipeline = [
        {
            "$match": {
                "station_id": station_id,
                "created_at": {"$gte": last_hour}
            }
        },
        {
            "$group": {
                "_id": None,
                "avg_crowd": {"$avg": "$crowd_level"}
            }
        }
    ]
    
    crowd_result = await db.crowd_reports.aggregate(pipeline).to_list(1)
    avg_crowd = crowd_result[0]["avg_crowd"] if crowd_result else None
    
    station_dict = {
        "id": str(station["_id"]),
        "name": station["name"],
        "line": station["line"],
        "latitude": station["latitude"],
        "longitude": station["longitude"],
        "station_type": station["station_type"],
        "created_at": station["created_at"],
        "current_crowd_level": round(float(avg_crowd), 2) if avg_crowd else None
    }
    
    return station_dict

@router.post("/", response_model=StationResponse)
async def create_station(
    station: StationCreate,
    current_user = Depends(get_current_user)
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Create station document
    station_dict = station.dict()
    station_dict["created_at"] = datetime.utcnow()
    
    result = await db.stations.insert_one(station_dict)
    
    # Return created station
    created_station = await db.stations.find_one({"_id": result.inserted_id})
    
    if not created_station:
        raise HTTPException(status_code=500, detail="Failed to create station")
    
    return {
        "id": str(created_station["_id"]),
        "name": created_station["name"],
        "line": created_station["line"],
        "latitude": created_station["latitude"],
        "longitude": created_station["longitude"],
        "station_type": created_station["station_type"],
        "created_at": created_station["created_at"],
        "current_crowd_level": None
    }