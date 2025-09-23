import React, { useEffect, useState } from "react";
import stationService from "../../services/stations";
import HeatMap from "./HeatMap";
import TrendChart from "./TrendChart";
import "./Analytics.css";

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const data = await stationService.getSystemOverview();
        setAnalytics(data);
      } catch (error) {
        console.error("Failed to load analytics", error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  if (!analytics) {
    return <div className="error">Analytics unavailable</div>;
  }

  const crowdedStations = analytics.most_crowded_stations ?? [];

  return (
    <div className="analytics">
      <h2>System Analytics</h2>

      <div className="analytics-summary">
        <p>Total Stations: {analytics.total_stations}</p>
        <p>Total Reports: {analytics.total_reports}</p>
        <p>Reports (24h): {analytics.reports_last_24h}</p>
      </div>

      <div className="analytics-highlights">
        <h3>Most Crowded Stations</h3>
        {crowdedStations.length ? (
          <ul>
            {crowdedStations.map((station) => (
              <li key={station.id}>
                {station.name} - average {station.average_crowd}
              </li>
            ))}
          </ul>
        ) : (
          <p className="no-data">No crowding data available</p>
        )}
      </div>

      <div className="analytics-visuals">
        <div className="heatmap-container">
          <h3>Crowd Heatmap</h3>
          <HeatMap />
        </div>

        <div className="trendchart-container">
          <h3>Crowd Trend (Simulated)</h3>
          <TrendChart />
        </div>
      </div>
    </div>
  );
};

export default Analytics;
