from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Station(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    line: str
    latitude: float
    longitude: float
    station_type: str = "metro"  # metro, bus, train
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "name": "Central Station",
                "line": "Red Line",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "station_type": "metro"
            }
        }
    }