from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:suro1234@localhost:5432/crowd_predictor"
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    WEATHER_API_KEY: Optional[str] = None
    TRANSIT_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()