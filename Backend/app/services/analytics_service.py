from datetime import datetime, timedelta
from typing import Dict
from bson import ObjectId

class AnalyticsService:
    async def get_station_analytics(
        self,
        db,
        station_id: str,
        days: int = 7
    ) -> Dict:
        """Get analytics for a specific station"""
        since = datetime.utcnow() - timedelta(days=days)
        
        # Validate station ID
        try:
            ObjectId(station_id)
        except Exception:
            return {"error": "Invalid station ID format"}
        
        # Get reports for the station
        cursor = db.crowd_reports.find({
            "station_id": station_id,
            "created_at": {"$gte": since}
        })
        reports = await cursor.to_list(length=1000)
        
        if not reports:
            return {
                "station_id": station_id,
                "period_days": days,
                "total_reports": 0,
                "average_crowd_level": 0,
                "peak_hours": [],
                "hourly_average": {}
            }
        
        # Calculate statistics
        crowd_levels = [r["crowd_level"] for r in reports]
        avg_crowd = sum(crowd_levels) / len(crowd_levels)
        
        # Group by hour
        hourly_data = {}
        for report in reports:
            hour = report["created_at"].hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(report["crowd_level"])
        
        hourly_avg = {
            hour: sum(levels)/len(levels) 
            for hour, levels in hourly_data.items()
        }
        
        # Find peak hours
        peak_threshold = avg_crowd + 0.5
        peak_hours = [
            hour for hour, avg in hourly_avg.items() 
            if avg >= peak_threshold
        ]
        
        return {
            "station_id": station_id,
            "period_days": days,
            "total_reports": len(reports),
            "average_crowd_level": round(avg_crowd, 2),
            "peak_hours": sorted(peak_hours),
            "hourly_average": {str(k): round(v, 2) for k, v in hourly_avg.items()},
            "max_crowd_level": max(crowd_levels),
            "min_crowd_level": min(crowd_levels)
        }
    
    async def get_system_overview(self, db) -> Dict:
        """Get system-wide analytics"""
        # Count total stations and reports
        total_stations = await db.stations.count_documents({})
        total_reports = await db.crowd_reports.count_documents({})
        
        # Recent activity
        last_24h = datetime.utcnow() - timedelta(hours=24)
        recent_reports = await db.crowd_reports.count_documents({
            "created_at": {"$gte": last_24h}
        })
        
        # Most crowded stations - using aggregation pipeline
        pipeline = [
            {
                "$group": {
                    "_id": "$station_id",
                    "avg_crowd": {"$avg": "$crowd_level"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$lookup": {
                    "from": "stations",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "station_info"
                }
            },
            {
                "$match": {
                    "station_info": {"$ne": []}
                }
            },
            {
                "$sort": {"avg_crowd": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        crowded_stations_cursor = db.crowd_reports.aggregate(pipeline)
        crowded_stations = await crowded_stations_cursor.to_list(5)
        
        # Format the results
        formatted_crowded_stations = []
        for station_data in crowded_stations:
            if station_data.get("station_info") and len(station_data["station_info"]) > 0:
                station_info = station_data["station_info"][0]
                formatted_crowded_stations.append({
                    "id": str(station_data["_id"]),
                    "name": station_info["name"],
                    "average_crowd": round(float(station_data["avg_crowd"]), 2)
                })
        
        return {
            "total_stations": total_stations,
            "total_reports": total_reports,
            "reports_last_24h": recent_reports,
            "most_crowded_stations": formatted_crowded_stations
        }

analytics_service = AnalyticsService()