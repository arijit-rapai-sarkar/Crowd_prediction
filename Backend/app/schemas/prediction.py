from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class PredictionBase(BaseModel):
    station_id: str
    predicted_crowd_level: float = Field(..., ge=1.0, le=5.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    prediction_time: datetime

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    id: str
    created_at: datetime
    factors: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    station_id: str
    hours_ahead: int = 1

class HourlyPredictionResponse(BaseModel):
    predictions: list[PredictionResponse]
    station_id: str