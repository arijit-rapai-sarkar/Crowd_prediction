from pydantic import BaseModel
from datetime import datetime
from typing import List

class PredictionBase(BaseModel):
    station_id: int
    predicted_crowd_level: float
    confidence_score: float
    prediction_time: datetime

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    station_id: int
    hours_ahead: int = 1