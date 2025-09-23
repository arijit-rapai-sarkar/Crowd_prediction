from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timedelta
from bson import ObjectId
from ..database import get_database
from ..models.crowd_report import CrowdReport
from ..models.station import Station
from ..schemas.crowd_report import CrowdReportCreate, CrowdReportResponse
from ..utils.dependencies import get_current_user

router = APIRouter(prefix="/api/crowd-reports", tags=["crowd-reports"])

@router.post("/", response_model=CrowdReportResponse)
async def create_crowd_report(
    report: CrowdReportCreate,
    current_user = Depends(get_current_user)
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Verify station exists
    try:
        station_obj_id = ObjectId(report.station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    station = await db.stations.find_one({"_id": station_obj_id})
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Create crowd report document
    report_dict = {
        "station_id": report.station_id,
        "user_id": str(current_user.id),
        "crowd_level": report.crowd_level,
        "description": report.description,
        "created_at": datetime.utcnow()
    }
    
    result = await db.crowd_reports.insert_one(report_dict)
    
    # Return created report
    created_report = await db.crowd_reports.find_one({"_id": result.inserted_id})
    if not created_report:
        raise HTTPException(status_code=500, detail="Failed to create crowd report")
    
    return {
        "id": str(created_report["_id"]),
        "station_id": created_report["station_id"],
        "user_id": created_report["user_id"],
        "crowd_level": created_report["crowd_level"],
        "description": created_report.get("description"),
        "created_at": created_report["created_at"]
    }

@router.get("/station/{station_id}", response_model=List[CrowdReportResponse])
async def get_station_reports(
    station_id: str,
    hours: int = 24
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Validate station ID
    try:
        ObjectId(station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    since = datetime.utcnow() - timedelta(hours=hours)
    cursor = db.crowd_reports.find({
        "station_id": station_id,
        "created_at": {"$gte": since}
    }).sort("created_at", -1)
    
    reports = await cursor.to_list(length=100)
    
    return [
        {
            "id": str(report["_id"]),
            "station_id": report["station_id"],
            "user_id": report["user_id"],
            "crowd_level": report["crowd_level"],
            "description": report.get("description"),
            "created_at": report["created_at"]
        }
        for report in reports
    ]

@router.get("/recent", response_model=List[CrowdReportResponse])
async def get_recent_reports(
    limit: int = 20
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    cursor = db.crowd_reports.find().sort("created_at", -1).limit(limit)
    reports = await cursor.to_list(length=limit)
    
    return [
        {
            "id": str(report["_id"]),
            "station_id": report["station_id"],
            "user_id": report["user_id"],
            "crowd_level": report["crowd_level"],
            "description": report.get("description"),
            "created_at": report["created_at"]
        }
        for report in reports
    ]