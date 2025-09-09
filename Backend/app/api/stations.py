from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Station, CrowdReport
from ..schemas.station import StationCreate, StationResponse
from ..utils.dependencies import get_current_user
from sqlalchemy import func
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/stations", tags=["stations"])

@router.get("/", response_model=List[StationResponse])
def get_stations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    stations = db.query(Station).offset(skip).limit(limit).all()
    
    # Add current crowd level
    result = []
    for station in stations:
        # Get average crowd level from last hour
        last_hour = datetime.now() - timedelta(hours=1)
        avg_crowd = db.query(func.avg(CrowdReport.crowd_level)).filter(
            CrowdReport.station_id == station.id,
            CrowdReport.created_at >= last_hour
        ).scalar()
        
        station_dict = {
            "id": station.id,
            "name": station.name,
            "line": station.line,
            "latitude": station.latitude,
            "longitude": station.longitude,
            "station_type": station.station_type,
            "created_at": station.created_at,
            "current_crowd_level": float(avg_crowd) if avg_crowd else None
        }
        result.append(station_dict)
    
    return result

@router.get("/{station_id}", response_model=StationResponse)
def get_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Get current crowd level
    last_hour = datetime.now() - timedelta(hours=1)
    avg_crowd = db.query(func.avg(CrowdReport.crowd_level)).filter(
        CrowdReport.station_id == station.id,
        CrowdReport.created_at >= last_hour
    ).scalar()
    
    station_dict = {
        "id": station.id,
        "name": station.name,
        "line": station.line,
        "latitude": station.latitude,
        "longitude": station.longitude,
        "station_type": station.station_type,
        "created_at": station.created_at,
        "current_crowd_level": float(avg_crowd) if avg_crowd else None
    }
    
    return station_dict

@router.post("/", response_model=StationResponse)
def create_station(
    station: StationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_station = Station(**station.dict())
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station