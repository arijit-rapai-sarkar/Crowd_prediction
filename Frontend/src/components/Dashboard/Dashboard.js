import React, { useEffect, useState } from "react";
import { getStations, getSystemAnalytics } from "../../services/stations";
import StationCard from "./StationCard";
import CrowdChart from "./CrowdChart";
import "./Dashboard.css";

const Dashboard = () => {
  const [stations, setStations] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const stationData = await getStations();
        const analyticsData = await getSystemAnalytics();
        setStations(stationData);
        setAnalytics(analyticsData);
      } catch (error) {
        console.error("Failed to load dashboard data", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (!analytics) return <div className="error">Failed to load data</div>;

  return (
    <div className="dashboard">
      <h2>Dashboard Overview</h2>
      <div className="dashboard-summary">
        <p>Total Stations: {analytics.total_stations}</p>
        <p>Total Reports: {analytics.total_reports}</p>
        <p>
          Most Crowded Station:{" "}
          {analytics.most_crowded_station
            ? analytics.most_crowded_station.name
            : "N/A"}
        </p>
      </div>

      <div className="dashboard-chart">
        <CrowdChart stations={stations} />
      </div>

      <h3>Stations</h3>
      <div className="dashboard-stations">
        {stations.map((station) => (
          <StationCard key={station.id} station={station} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
