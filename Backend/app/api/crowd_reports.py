from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import CrowdReport, Station
from ..schemas.crowd_report import CrowdReportCreate, CrowdReportResponse
from ..utils.dependencies import get_current_user
from ..services.weather_service import weather_service

router = APIRouter(prefix="/api/crowd-reports", tags=["crowd-reports"])

@router.post("/", response_model=CrowdReportResponse)
async def create_crowd_report(
    report: CrowdReportCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Verify station exists
    station = db.query(Station).filter(Station.id == report.station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Get weather data
    weather_data = await weather_service.get_weather(
        station.latitude, 
        station.longitude
    )
    
    db_report = CrowdReport(
        station_id=report.station_id,
        user_id=current_user.id,
        crowd_level=report.crowd_level,
        description=report.description,
        temperature=weather_data["temperature"] if weather_data else None,
        weather_condition=weather_data["condition"] if weather_data else None
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@router.get("/station/{station_id}", response_model=List[CrowdReportResponse])
def get_station_reports(
    station_id: int,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    since = datetime.now() - timedelta(hours=hours)
    reports = db.query(CrowdReport).filter(
        CrowdReport.station_id == station_id,
        CrowdReport.created_at >= since
    ).order_by(CrowdReport.created_at.desc()).all()
    
    return reports

@router.get("/recent", response_model=List[CrowdReportResponse])
def get_recent_reports(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    reports = db.query(CrowdReport).order_by(
        CrowdReport.created_at.desc()
    ).limit(limit).all()
    
    return reports