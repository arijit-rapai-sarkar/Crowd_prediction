import React, { useEffect, useState } from "react";
import stationService from "../../services/stations";
import StationCard from "./StationCard";
import CrowdChart from "./CrowdChart";
import "./Dashboard.css";

const Dashboard = () => {
  const [stations, setStations] = useState([]);
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [stationData, overviewData] = await Promise.all([
          stationService.getAll(),
          stationService.getSystemOverview(),
        ]);
        setStations(stationData);
        setOverview(overviewData);
      } catch (error) {
        console.error("Failed to load dashboard data", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  if (!overview) {
    return <div className="error">Unable to load dashboard data</div>;
  }

  const crowdedStations = overview.most_crowded_stations ?? [];

  return (
    <div className="dashboard">
      <h2>Transit Network Overview</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Stations</h3>
          <span className="stat-value">{overview.total_stations}</span>
        </div>
        <div className="stat-card">
          <h3>Total Reports</h3>
          <span className="stat-value">{overview.total_reports}</span>
        </div>
        <div className="stat-card">
          <h3>Reports (24h)</h3>
          <span className="stat-value">{overview.reports_last_24h}</span>
        </div>
        <div className="stat-card">
          <h3>Most Crowded</h3>
          <span className="stat-value">
            {crowdedStations.length ? crowdedStations[0].name : "N/A"}
          </span>
        </div>
      </div>

      <div className="dashboard-content">
        <div className="stations-section">
          <h3>Live Station Snapshot</h3>
          <div className="stations-grid">
            {stations.slice(0, 6).map((station) => (
              <StationCard key={station.id} station={station} />
            ))}
          </div>
        </div>

        <div className="chart-section">
          <h3>Crowd Levels Across Stations</h3>
          <CrowdChart stations={stations} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
