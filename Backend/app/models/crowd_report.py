from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CrowdReport(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    station_id: str  # Reference to Station ObjectId as string
    user_id: str  # Reference to User ObjectId as string
    crowd_level: int = Field(..., ge=1, le=5)  # 1-5 scale with validation
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "station_id": "60f1b2c3d4e5f6g7h8i9j0k1",
                "user_id": "60f1b2c3d4e5f6g7h8i9j0k2",
                "crowd_level": 3,
                "description": "Moderate crowd during rush hour"
            }
        }
    }