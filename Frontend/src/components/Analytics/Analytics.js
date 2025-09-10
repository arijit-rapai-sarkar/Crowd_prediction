import React, { useEffect, useState } from "react";
import { getSystemAnalytics } from "../../services/stations";
import HeatMap from "./HeatMap";
import TrendChart from "./TreandChart";
import "./Analytics.css";

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getSystemAnalytics();
        setAnalytics(data);
      } catch (error) {
        console.error("Failed to load analytics", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) return <div className="loading">Loading analytics...</div>;
  if (!analytics) return <div className="error">Failed to load analytics</div>;

  return (
    <div className="analytics">
      <h2>System Analytics</h2>
      <div className="analytics-summary">
        <p>Total Stations: {analytics.total_stations}</p>
        <p>Total Reports: {analytics.total_reports}</p>
        <p>
          Most Crowded Station:{" "}
          {analytics.most_crowded_station
            ? analytics.most_crowded_station.name
            : "N/A"}
        </p>
      </div>

      <div className="analytics-visuals">
        <div className="heatmap-container">
          <h3>Crowd Heatmap</h3>
          <HeatMap />
        </div>

        <div className="trendchart-container">
          <h3>Crowd Trends</h3>
          <TrendChart />
        </div>
      </div>
    </div>
  );
};

export default Analytics;
