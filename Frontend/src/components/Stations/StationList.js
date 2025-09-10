import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getStations } from "../../services/stations";
import { CROWD_COLORS, CROWD_LEVELS } from "../../utils/constants";
import "./Stations.css";

const StationList = () => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStations = async () => {
      try {
        const data = await getStations();
        setStations(data);
      } catch (error) {
        console.error("Failed to fetch stations", error);
      } finally {
        setLoading(false);
      }
    };
    fetchStations();
  }, []);

  if (loading) return <div className="loading">Loading stations...</div>;

  return (
    <div className="stations">
      <h2>Stations</h2>
      <div className="stations-grid">
        {stations.map((station) => {
          const level = station.current_crowd_level || 3;
          return (
            <Link
              to={`/stations/${station.id}`}
              key={station.id}
              className="station-card"
            >
              <h3>{station.name}</h3>
              <p style={{ color: CROWD_COLORS[level] }}>
                {CROWD_LEVELS[level]} ({level})
              </p>
              <small>Type: {station.type}</small>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default StationList;
