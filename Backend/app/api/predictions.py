# backend/app/api/predictions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Prediction, Station, CrowdReport
from ..schemas.prediction import PredictionResponse, PredictionRequest
from ..services.prediction_service import prediction_service
from ..services.weather_service import weather_service

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.post("/predict", response_model=PredictionResponse)
async def create_prediction(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    # Verify station exists
    station = db.query(Station).filter(Station.id == request.station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Get historical data
    since = datetime.now() - timedelta(days=7)
    historical_reports = db.query(CrowdReport).filter(
        CrowdReport.station_id == request.station_id,
        CrowdReport.created_at >= since
    ).all()
    
    # Get weather data
    weather_data = await weather_service.get_weather(
        station.latitude,
        station.longitude
    )
    
    # Generate prediction
    target_time = datetime.now() + timedelta(hours=request.hours_ahead)
    prediction_result = prediction_service.predict_crowd_level(
        station_id=request.station_id,
        target_time=target_time,
        historical_data=[{
            "crowd_level": r.crowd_level,
            "created_at": r.created_at
        } for r in historical_reports],
        weather_data=weather_data
    )
    
    # Save prediction
    db_prediction = Prediction(
        station_id=request.station_id,
        predicted_crowd_level=prediction_result["predicted_crowd_level"],
        confidence_score=prediction_result["confidence_score"],
        prediction_time=target_time
    )
    
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    
    return db_prediction

@router.get("/hourly/{station_id}")
def get_hourly_predictions(
    station_id: int,
    hours: int = 24,
    db: Session = Depends(get_db)
):
    # Verify station exists
    station = db.query(Station).filter(Station.id == station_id).first()
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    predictions = prediction_service.get_hourly_predictions(
        station_id=station_id,
        hours_ahead=hours
    )
    
    return {"station_id": station_id, "predictions": predictions}

@router.get("/station/{station_id}", response_model=List[PredictionResponse])
def get_station_predictions(
    station_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    predictions = db.query(Prediction).filter(
        Prediction.station_id == station_id
    ).order_by(Prediction.created_at.desc()).limit(limit).all()
    
    return predictions
