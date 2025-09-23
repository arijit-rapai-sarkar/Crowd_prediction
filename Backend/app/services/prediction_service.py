import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import os
from ..database import get_database

class CrowdPredictionService:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = [
            'hour', 'day_of_week', 'is_weekend', 'month',
            'is_rush_hour', 'is_morning_rush', 'is_evening_rush',
            'historical_avg', 'recent_trend'
        ]
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model or initialize a new one"""
        model_path = "crowd_prediction_model.pkl"
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.scaler = data['scaler']
        else:
            # Initialize with default RandomForest
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
    
    def save_model(self):
        """Save trained model to disk"""
        model_path = "crowd_prediction_model.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler
            }, f)
    
    def extract_time_features(self, target_time: datetime) -> Dict:
        """Extract time-based features from datetime"""
        hour = target_time.hour
        day_of_week = target_time.weekday()
        month = target_time.month
        
        is_weekend = day_of_week >= 5
        is_morning_rush = 7 <= hour <= 10 and not is_weekend
        is_evening_rush = 17 <= hour <= 20 and not is_weekend
        is_rush_hour = is_morning_rush or is_evening_rush
        
        return {
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': int(is_weekend),
            'month': month,
            'is_rush_hour': int(is_rush_hour),
            'is_morning_rush': int(is_morning_rush),
            'is_evening_rush': int(is_evening_rush)
        }
    
    async def get_historical_data(self, station_id: str, days_back: int = 30) -> List[Dict]:
        """Retrieve historical crowd data for a station"""
        db = get_database()
        if db is None:
            return []
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        cursor = db.crowd_reports.find({
            "station_id": station_id,
            "created_at": {"$gte": cutoff_date}
        }).sort("created_at", -1)
        
        return await cursor.to_list(length=1000)
    
    def calculate_historical_features(self, historical_data: List[Dict], target_time: datetime) -> Dict:
        """Calculate features based on historical data"""
        if not historical_data:
            return {'historical_avg': 2.5, 'recent_trend': 0}
        
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(historical_data)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['hour'] = df['created_at'].dt.hour
        df['day_of_week'] = df['created_at'].dt.dayofweek
        
        # Calculate historical average for similar time periods
        similar_hours = df[df['hour'] == target_time.hour]
        historical_avg = similar_hours['crowd_level'].mean() if len(similar_hours) > 0 else 2.5
        
        # Calculate recent trend (last 7 days vs previous 7 days)
        recent_cutoff = datetime.utcnow() - timedelta(days=7)
        recent_data = df[df['created_at'] >= recent_cutoff]
        older_data = df[df['created_at'] < recent_cutoff]
        
        recent_avg = recent_data['crowd_level'].mean() if len(recent_data) > 0 else historical_avg
        older_avg = older_data['crowd_level'].mean() if len(older_data) > 0 else historical_avg
        
        recent_trend = recent_avg - older_avg
        
        return {
            'historical_avg': float(historical_avg),
            'recent_trend': float(recent_trend)
        }
    
    async def predict_crowd_level(
        self, 
        station_id: str, 
        target_time: datetime
    ) -> Dict:
        """
        Predict crowd level for a station at a specific time using ML
        """
        try:
            # Extract time features
            time_features = self.extract_time_features(target_time)
            
            # Get historical data
            historical_data = await self.get_historical_data(station_id)
            historical_features = self.calculate_historical_features(historical_data, target_time)
            
            # Combine all features
            features = {**time_features, **historical_features}
            
            # Create feature vector
            feature_vector = np.array([[features[col] for col in self.feature_columns]])
            
            # Make prediction
            if self.model is not None and hasattr(self.model, 'predict'):
                try:
                    scaled_features = self.scaler.transform(feature_vector)
                    predicted_crowd = self.model.predict(scaled_features)[0]
                    confidence = 0.8  # Model-based confidence
                except Exception:
                    # Fallback to rule-based prediction
                    predicted_crowd = self._rule_based_prediction(features)
                    confidence = 0.6
            else:
                # Use rule-based prediction
                predicted_crowd = self._rule_based_prediction(features)
                confidence = 0.6
            
            # Ensure prediction is within valid range
            predicted_crowd = max(1.0, min(5.0, float(predicted_crowd)))
            
            # Calculate confidence based on data availability
            if len(historical_data) > 50:
                confidence += 0.1
            elif len(historical_data) > 20:
                confidence += 0.05
            
            confidence = min(1.0, confidence)
            
            return {
                "predicted_crowd_level": round(predicted_crowd, 2),
                "confidence_score": round(confidence, 2),
                "factors": {
                    "time_of_day": "rush" if features['is_rush_hour'] else "normal",
                    "day_type": "weekend" if features['is_weekend'] else "weekday",
                    "historical_average": round(features['historical_avg'], 2),
                    "recent_trend": "increasing" if features['recent_trend'] > 0.1 else 
                                  "decreasing" if features['recent_trend'] < -0.1 else "stable"
                },
                "prediction_time": target_time.isoformat()
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback prediction
            return self._fallback_prediction(target_time)
    
    def _rule_based_prediction(self, features: Dict) -> float:
        """Rule-based prediction as fallback"""
        base_crowd = features['historical_avg']
        
        # Adjust for time patterns
        if features['is_morning_rush']:
            base_crowd += 1.0
        elif features['is_evening_rush']:
            base_crowd += 1.2
        elif features['is_weekend'] and 11 <= features['hour'] <= 20:
            base_crowd += 0.5
        
        # Apply recent trend
        base_crowd += features['recent_trend'] * 0.5
        
        return base_crowd
    
    def _fallback_prediction(self, target_time: datetime) -> Dict:
        """Simple fallback prediction when all else fails"""
        hour = target_time.hour
        is_weekend = target_time.weekday() >= 5
        
        if not is_weekend and (7 <= hour <= 10 or 17 <= hour <= 20):
            crowd_level = 4.0
        elif is_weekend and 11 <= hour <= 20:
            crowd_level = 3.0
        else:
            crowd_level = 2.0
        
        return {
            "predicted_crowd_level": crowd_level,
            "confidence_score": 0.5,
            "factors": {
                "time_of_day": "rush" if (7 <= hour <= 10 or 17 <= hour <= 20) and not is_weekend else "normal",
                "day_type": "weekend" if is_weekend else "weekday",
                "note": "fallback_prediction"
            },
            "prediction_time": target_time.isoformat()
        }
    
    async def get_hourly_predictions(
        self,
        station_id: str,
        hours_ahead: int = 24
    ) -> List[Dict]:
        """Get hourly predictions for the next N hours"""
        predictions = []
        current_time = datetime.utcnow()
        
        for i in range(hours_ahead):
            target_time = current_time + timedelta(hours=i)
            pred = await self.predict_crowd_level(station_id, target_time)
            predictions.append(pred)
        
        return predictions
    
    async def train_model_with_data(self, station_id: Optional[str] = None):
        """Train the model with available historical data"""
        db = get_database()
        if db is None:
            return False
        
        # Get training data
        query = {"station_id": station_id} if station_id else {}
        cursor = db.crowd_reports.find(query)
        data = await cursor.to_list(length=10000)
        
        if len(data) < 50:  # Minimum data requirement
            print(f"Insufficient data for training: {len(data)} records")
            return False
        
        # Prepare training data
        X = []
        y = []
        
        for report in data:
            created_at = report['created_at']
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            
            time_features = self.extract_time_features(created_at)
            
            # Get historical context for this report
            historical_data = [r for r in data if r['created_at'] < report['created_at']]
            historical_features = self.calculate_historical_features(historical_data, created_at)
            
            features = {**time_features, **historical_features}
            feature_vector = [features[col] for col in self.feature_columns]
            
            X.append(feature_vector)
            y.append(report['crowd_level'])
        
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize model if not already done
        if self.model is None:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Model trained - Train Score: {train_score:.3f}, Test Score: {test_score:.3f}")
        
        # Save model
        self.save_model()
        
        return True

prediction_service = CrowdPredictionService()