from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StationBase(BaseModel):
    name: str
    line: str
    latitude: float
    longitude: float
    station_type: str = "metro"

class StationCreate(StationBase):
    pass

class StationResponse(StationBase):
    id: str
    created_at: datetime
    current_crowd_level: Optional[float] = None
    
    class Config:
        from_attributes = True