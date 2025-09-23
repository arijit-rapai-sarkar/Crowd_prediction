import React, { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import stationService from "../../services/stations";
import CrowdReportForm from "./CrowdReportForm";
import { CROWD_LEVELS, CHART_COLORS, DEFAULT_MAP_CENTER } from "../../utils/constants";
import "./Stations.css";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png",
  iconUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png",
  shadowUrl:
    "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
});

const StationDetail = () => {
  const { id } = useParams();
  const [station, setStation] = useState(null);
  const [reports, setReports] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showReportForm, setShowReportForm] = useState(false);

  const fetchStationData = useCallback(async () => {
    try {
      setLoading(true);
      const [stationData, reportsData, predictionsData, analyticsData] =
        await Promise.all([
          stationService.getById(id),
          stationService.getStationReports(id, 24),
          stationService.getHourlyPredictions(id, 24),
          stationService.getStationAnalytics(id, 7),
        ]);

      setStation(stationData);
      setReports(reportsData);
      setPredictions(predictionsData?.predictions ?? []);
      setAnalytics(analyticsData);
    } catch (error) {
      console.error("Error fetching station data", error);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchStationData();
  }, [fetchStationData]);

  const handleReportSubmit = async (crowdLevel, description) => {
    try {
      await stationService.createCrowdReport(id, crowdLevel, description);
      setShowReportForm(false);
      await fetchStationData();
    } catch (error) {
      console.error("Error submitting report", error);
    }
  };

  if (loading) {
    return <div className="loading">Loading station details...</div>;
  }

  if (!station) {
    return <div className="error">Station not found</div>;
  }

  const crowdLevel = station.current_crowd_level
    ? Math.round(station.current_crowd_level)
    : null;
  const crowdInfo = crowdLevel ? CROWD_LEVELS[crowdLevel] : null;
  const hasCoordinates = typeof station.latitude === "number" && typeof station.longitude === "number";
  const mapCenter = hasCoordinates ? [station.latitude, station.longitude] : DEFAULT_MAP_CENTER;

  const chartData = {
    labels: predictions.map((prediction) =>
      new Date(prediction.time).toLocaleTimeString([], { hour: "2-digit" })
    ),
    datasets: [
      {
        label: "Predicted Crowd Level",
        data: predictions.map((prediction) => prediction.predicted_crowd_level),
        borderColor: CHART_COLORS.primary,
        backgroundColor: CHART_COLORS.primaryBg,
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Next 24 Hours" },
    },
    scales: {
      y: {
        min: 0,
        max: 5,
        ticks: { stepSize: 1 },
      },
    },
  };

  return (
    <div className="station-detail">
      <div className="detail-header">
        <div>
          <h2>{station.name}</h2>
          <p className="station-meta">
            {station.line} - {station.station_type}
          </p>
        </div>
        <button
          className="report-btn"
          onClick={() => setShowReportForm(true)}
        >
          Report Crowd Level
        </button>
      </div>

      <div className="detail-grid">
        <div className="detail-section">
          <h3>Current Status</h3>
          <div className="current-status">
            {crowdInfo ? (
              <>
                <div
                  className="status-indicator"
                  style={{ backgroundColor: crowdInfo.color }}
                >
                  {crowdInfo.label}
                </div>
                <p>Crowd Level: {station.current_crowd_level?.toFixed(1)}/5</p>
              </>
            ) : (
              <p className="no-data">No recent reports available</p>
            )}
          </div>
        </div>

        <div className="detail-section">
          <h3>Station Analytics (7 days)</h3>
          {analytics ? (
            <div className="analytics-stats">
              <div className="stat">
                <span className="stat-label">Total Reports:</span>
                <span className="stat-value">{analytics.total_reports}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Average Crowd:</span>
                <span className="stat-value">{analytics.average_crowd_level}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Peak Hours:</span>
                <span className="stat-value">
                  {analytics.peak_hours?.length
                    ? analytics.peak_hours.join(", ")
                    : "N/A"}
                </span>
              </div>
            </div>
          ) : (
            <p className="no-data">Analytics unavailable</p>
          )}
        </div>
      </div>

      <div className="chart-section">
        {predictions.length > 0 ? (
          <Line data={chartData} options={chartOptions} />
        ) : (
          <p className="no-data">No predictions available</p>
        )}
      </div>

      <div className="map-section">
        <h3>Station Location</h3>
        <div className="map-container">
          <MapContainer
            center={mapCenter || DEFAULT_MAP_CENTER}
            zoom={15}
            style={{ height: "300px", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            {hasCoordinates && (
              <Marker position={[station.latitude, station.longitude]}>
                <Popup>
                  {station.name}
                  <br />
                  {station.line}
                </Popup>
              </Marker>
            )}
          </MapContainer>
        </div>
      </div>

      <div className="recent-reports">
        <h3>Recent Reports</h3>
        {reports.length > 0 ? (
          <div className="reports-list">
            {reports.slice(0, 5).map((report) => {
              const levelInfo = CROWD_LEVELS[report.crowd_level] || CROWD_LEVELS[3];
              return (
                <div key={report.id} className="report-item">
                  <div className="report-level">
                    <span
                      className="level-badge"
                      style={{
                        backgroundColor: `${levelInfo.color}20`,
                        color: levelInfo.color,
                      }}
                    >
                      {levelInfo.label}
                    </span>
                  </div>
                  <div className="report-details">
                    {report.description && <p>{report.description}</p>}
                    <span className="report-time">
                      {new Date(report.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <p className="no-data">No reports yet</p>
        )}
      </div>

      {showReportForm && (
        <CrowdReportForm
          onSubmit={handleReportSubmit}
          onClose={() => setShowReportForm(false)}
        />
      )}
    </div>
  );
};

export default StationDetail;






