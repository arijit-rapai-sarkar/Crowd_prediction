from fastapi import APIRouter, HTTPException
from ..database import get_database
from ..services.analytics_service import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/station/{station_id}")
async def get_station_analytics(
    station_id: str,
    days: int = 7
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    return await analytics_service.get_station_analytics(db, station_id, days)

@router.get("/overview")
async def get_system_overview():
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    return await analytics_service.get_system_overview(db)