import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import {
  getStation,
  getStationPredictions,
  getStationAnalytics,
} from "../../services/stations";
import CrowdReportForm from "./CrowdReportForm";
import { CROWD_COLORS, CROWD_LEVELS } from "../../utils/constants";
import { Line } from "react-chartjs-2";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";
import "leaflet/dist/leaflet.css";
import "./Stations.css";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

const StationDetail = () => {
  const { id } = useParams();
  const [station, setStation] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [showReportForm, setShowReportForm] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const stationData = await getStation(id);
        const predictionData = await getStationPredictions(id);
        const analyticsData = await getStationAnalytics(id);
        setStation(stationData);
        setPredictions(predictionData);
        setAnalytics(analyticsData);
      } catch (error) {
        console.error("Failed to load station details", error);
      }
    };
    fetchData();
  }, [id]);

  if (!station) return <div className="loading">Loading station details...</div>;

  const chartData = {
    labels: predictions.map((p) =>
      new Date(p.prediction_time).toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    ),
    datasets: [
      {
        label: "Predicted Crowd Level",
        data: predictions.map((p) => p.predicted_crowd_level),
        borderColor: "#42a5f5",
        backgroundColor: "rgba(66, 165, 245, 0.2)",
        tension: 0.3,
      },
    ],
  };

  return (
    <div className="station-detail">
      <h2>{station.name}</h2>
      <p>
        Current Crowd Level:{" "}
        <span style={{ color: CROWD_COLORS[station.current_crowd_level || 3] }}>
          {CROWD_LEVELS[station.current_crowd_level || 3]}
        </span>
      </p>

      <div className="station-chart">
        <h3>24-Hour Predictions</h3>
        <Line data={chartData} />
      </div>

      <div className="station-map">
        <h3>Location</h3>
        <MapContainer
          center={[station.latitude, station.longitude]}
          zoom={14}
          style={{ height: "300px", width: "100%" }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution="© OpenStreetMap contributors"
          />
          <Marker position={[station.latitude, station.longitude]}>
            <Popup>{station.name}</Popup>
          </Marker>
        </MapContainer>
      </div>

      {analytics && (
        <div className="station-analytics">
          <h3>Analytics (7 days)</h3>
          <p>Average Crowd Level: {analytics.avg_crowd_level}</p>
          <p>Peak Hours: {analytics.peak_hours.join(", ")}</p>
        </div>
      )}

      <button onClick={() => setShowReportForm(true)} className="report-btn">
        Submit Crowd Report
      </button>

      {showReportForm && (
        <CrowdReportForm
          stationId={id}
          onClose={() => setShowReportForm(false)}
        />
      )}
    </div>
  );
};

export default StationDetail;
