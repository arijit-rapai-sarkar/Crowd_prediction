# backend/app/api/predictions.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime, timedelta
from bson import ObjectId
from ..database import get_database
from ..models.prediction import Prediction
from ..models.station import Station
from ..schemas.prediction import PredictionResponse, PredictionRequest, HourlyPredictionResponse
from ..services.prediction_service import prediction_service

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.post("/predict", response_model=PredictionResponse)
async def create_prediction(
    request: PredictionRequest
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Verify station exists
    try:
        station_obj_id = ObjectId(request.station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    station = await db.stations.find_one({"_id": station_obj_id})
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Generate prediction using the enhanced prediction service
    target_time = datetime.utcnow() + timedelta(hours=request.hours_ahead)
    prediction_result = await prediction_service.predict_crowd_level(
        station_id=request.station_id,
        target_time=target_time
    )
    
    # Save prediction to database
    prediction_dict = {
        "station_id": request.station_id,
        "predicted_crowd_level": prediction_result["predicted_crowd_level"],
        "confidence_score": prediction_result["confidence_score"],
        "prediction_time": target_time,
        "created_at": datetime.utcnow()
    }
    
    result = await db.predictions.insert_one(prediction_dict)
    
    # Return the prediction with factors
    return {
        "id": str(result.inserted_id),
        "station_id": request.station_id,
        "predicted_crowd_level": prediction_result["predicted_crowd_level"],
        "confidence_score": prediction_result["confidence_score"],
        "prediction_time": target_time,
        "created_at": prediction_dict["created_at"],
        "factors": prediction_result.get("factors")
    }

@router.get("/hourly/{station_id}")
async def get_hourly_predictions(
    station_id: str,
    hours: int = 24
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Verify station exists
    try:
        station_obj_id = ObjectId(station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    station = await db.stations.find_one({"_id": station_obj_id})
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    predictions = await prediction_service.get_hourly_predictions(
        station_id=station_id,
        hours_ahead=hours
    )
    
    return {"station_id": station_id, "predictions": predictions}

@router.get("/station/{station_id}", response_model=List[PredictionResponse])
async def get_station_predictions(
    station_id: str,
    limit: int = 10
):
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Validate station ID
    try:
        ObjectId(station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    cursor = db.predictions.find({
        "station_id": station_id
    }).sort("created_at", -1).limit(limit)
    
    predictions = await cursor.to_list(length=limit)
    
    return [
        {
            "id": str(pred["_id"]),
            "station_id": pred["station_id"],
            "predicted_crowd_level": pred["predicted_crowd_level"],
            "confidence_score": pred["confidence_score"],
            "prediction_time": pred["prediction_time"],
            "created_at": pred["created_at"],
            "factors": pred.get("factors")
        }
        for pred in predictions
    ]

@router.post("/train/{station_id}")
async def train_model_for_station(station_id: str):
    """Train the prediction model with data for a specific station"""
    db = get_database()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Verify station exists
    try:
        station_obj_id = ObjectId(station_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid station ID format")
    
    station = await db.stations.find_one({"_id": station_obj_id})
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Train model
    success = await prediction_service.train_model_with_data(station_id)
    
    if success:
        return {"message": f"Model trained successfully for station {station_id}"}
    else:
        raise HTTPException(status_code=400, detail="Insufficient data for training")

@router.post("/train-all")
async def train_model_all_stations():
    """Train the prediction model with data from all stations"""
    success = await prediction_service.train_model_with_data()
    
    if success:
        return {"message": "Model trained successfully with all station data"}
    else:
        raise HTTPException(status_code=400, detail="Insufficient data for training")
