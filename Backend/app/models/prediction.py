from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Prediction(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    station_id: str  # Reference to Station ObjectId as string
    predicted_crowd_level: float = Field(..., ge=1.0, le=5.0)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    prediction_time: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "station_id": "60f1b2c3d4e5f6g7h8i9j0k1",
                "predicted_crowd_level": 3.5,
                "confidence_score": 0.85,
                "prediction_time": "2025-09-24T14:30:00Z"
            }
        }
    }