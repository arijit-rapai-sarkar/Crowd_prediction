from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/station/{station_id}")
def get_station_analytics(
    station_id: int,
    days: int = 7,
    db: Session = Depends(get_db)
):
    return analytics_service.get_station_analytics(db, station_id, days)

@router.get("/overview")
def get_system_overview(db: Session = Depends(get_db)):
    return analytics_service.get_system_overview(db)