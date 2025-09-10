import React from "react";
import { Link } from "react-router-dom";
import { CROWD_LEVELS, CROWD_COLORS } from "../../utils/constants";
import "./Dashboard.css";

const StationCard = ({ station }) => {
  const level = station.current_crowd_level || 3;

  return (
    <Link to={`/stations/${station.id}`} className="station-card">
      <h4>{station.name}</h4>
      <p style={{ color: CROWD_COLORS[level] }}>
        {CROWD_LEVELS[level]} ({level})
      </p>
      <small>Type: {station.type}</small>
    </Link>
  );
};

export default StationCard;
