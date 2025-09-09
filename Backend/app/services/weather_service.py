import httpx
from typing import Optional
from ..config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    async def get_weather(self, lat: float, lon: float) -> Optional[dict]:
        if not self.api_key:
            return None
        
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "temperature": data["main"]["temp"],
                        "condition": data["weather"][0]["main"],
                        "humidity": data["main"]["humidity"]
                    }
        except Exception as e:
            print(f"Weather API error: {e}")
        
        return None

weather_service = WeatherService()