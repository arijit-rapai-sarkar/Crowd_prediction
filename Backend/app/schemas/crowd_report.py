from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CrowdReportBase(BaseModel):
    station_id: int
    crowd_level: int = Field(..., ge=1, le=5)
    description: Optional[str] = None

class CrowdReportCreate(CrowdReportBase):
    pass

class CrowdReportResponse(CrowdReportBase):
    id: int
    user_id: int
    temperature: Optional[float] = None
    weather_condition: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True