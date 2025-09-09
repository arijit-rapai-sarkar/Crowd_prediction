import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

class PredictionService:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        # For demo, we'll use a simple rule-based prediction
        # In production, load a trained ML model
        pass
    
    def predict_crowd_level(
        self, 
        station_id: int, 
        target_time: datetime,
        historical_data: List[dict],
        weather_data: Optional[dict] = None
    ) -> dict:
        """
        Predict crowd level for a station at a specific time
        """
        # Extract features
        hour = target_time.hour
        day_of_week = target_time.weekday()
        is_weekend = day_of_week >= 5
        
        # Simple rule-based prediction for demo
        # Rush hours: 7-10 AM and 5-8 PM on weekdays
        if not is_weekend:
            if 7 <= hour < 10:
                base_crowd = 4.0 + np.random.uniform(-0.5, 0.5)
            elif 17 <= hour < 20:
                base_crowd = 4.5 + np.random.uniform(-0.5, 0.5)
            elif 10 <= hour < 17:
                base_crowd = 2.5 + np.random.uniform(-0.5, 0.5)
            else:
                base_crowd = 1.5 + np.random.uniform(-0.5, 0.5)
        else:
            # Weekend patterns
            if 11 <= hour < 20:
                base_crowd = 3.0 + np.random.uniform(-0.5, 0.5)
            else:
                base_crowd = 2.0 + np.random.uniform(-0.5, 0.5)
        
        # Weather adjustment
        if weather_data:
            if weather_data.get("condition") == "Rain":
                base_crowd += 0.5
            elif weather_data.get("temperature", 20) > 35:
                base_crowd += 0.3
        
        # Ensure crowd level is between 1 and 5
        predicted_crowd = max(1.0, min(5.0, base_crowd))
        
        # Calculate confidence based on data availability
        confidence = 0.85 if historical_data else 0.65
        if weather_data:
            confidence += 0.05
        
        return {
            "predicted_crowd_level": round(predicted_crowd, 2),
            "confidence_score": round(confidence, 2),
            "factors": {
                "time_of_day": "rush" if (7 <= hour < 10 or 17 <= hour < 20) and not is_weekend else "normal",
                "day_type": "weekend" if is_weekend else "weekday",
                "weather_impact": weather_data.get("condition") if weather_data else "unknown"
            }
        }
    
    def get_hourly_predictions(
        self,
        station_id: int,
        hours_ahead: int = 24
    ) -> List[dict]:
        """
        Get hourly predictions for the next N hours
        """
        predictions = []
        current_time = datetime.now()
        
        for i in range(hours_ahead):
            target_time = current_time + timedelta(hours=i)
            pred = self.predict_crowd_level(
                station_id=station_id,
                target_time=target_time,
                historical_data=[]  # Would fetch from DB in production
            )
            pred["time"] = target_time.isoformat()
            predictions.append(pred)
        
        return predictions

prediction_service = PredictionService()