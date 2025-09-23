from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CrowdReportBase(BaseModel):
    station_id: str
    crowd_level: int = Field(..., ge=1, le=5)
    description: Optional[str] = None

class CrowdReportCreate(CrowdReportBase):
    pass

class CrowdReportResponse(CrowdReportBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True