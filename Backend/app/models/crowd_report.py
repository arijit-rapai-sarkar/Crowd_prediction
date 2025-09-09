from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class CrowdReport(Base):
    __tablename__ = "crowd_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    crowd_level = Column(Integer, nullable=False)  # 1-5 scale
    description = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    weather_condition = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    station = relationship("Station")
    user = relationship("User")