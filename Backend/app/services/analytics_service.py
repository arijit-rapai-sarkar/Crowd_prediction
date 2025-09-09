from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List, Dict
from ..models import CrowdReport, Station

class AnalyticsService:
    def get_station_analytics(
        self,
        db: Session,
        station_id: int,
        days: int = 7
    ) -> Dict:
        """Get analytics for a specific station"""
        since = datetime.now() - timedelta(days=days)
        
        reports = db.query(CrowdReport).filter(
            and_(
                CrowdReport.station_id == station_id,
                CrowdReport.created_at >= since
            )
        ).all()
        
        if not reports:
            return {
                "station_id": station_id,
                "period_days": days,
                "total_reports": 0,
                "average_crowd_level": 0,
                "peak_hours": [],
                "daily_pattern": []
            }
        
        # Calculate statistics
        crowd_levels = [r.crowd_level for r in reports]
        avg_crowd = sum(crowd_levels) / len(crowd_levels)
        
        # Group by hour
        hourly_data = {}
        for report in reports:
            hour = report.created_at.hour
            if hour not in hourly_data:
                hourly_data[hour] = []
            hourly_data[hour].append(report.crowd_level)
        
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
            "hourly_average": hourly_avg,
            "max_crowd_level": max(crowd_levels),
            "min_crowd_level": min(crowd_levels)
        }
    
    def get_system_overview(self, db: Session) -> Dict:
        """Get system-wide analytics"""
        total_stations = db.query(Station).count()
        total_reports = db.query(CrowdReport).count()
        
        # Recent activity
        last_24h = datetime.now() - timedelta(hours=24)
        recent_reports = db.query(CrowdReport).filter(
            CrowdReport.created_at >= last_24h
        ).count()
        
        # Most crowded stations
        crowded_stations = db.query(
            Station.id,
            Station.name,
            func.avg(CrowdReport.crowd_level).label('avg_crowd')
        ).join(
            CrowdReport
        ).group_by(
            Station.id, Station.name
        ).order_by(
            func.avg(CrowdReport.crowd_level).desc()
        ).limit(5).all()
        
        return {
            "total_stations": total_stations,
            "total_reports": total_reports,
            "reports_last_24h": recent_reports,
            "most_crowded_stations": [
                {
                    "id": s[0],
                    "name": s[1],
                    "average_crowd": round(float(s[2]), 2)
                }
                for s in crowded_stations
            ]
        }

analytics_service = AnalyticsService()