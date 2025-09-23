import React from "react";
import { Link } from "react-router-dom";
import { CROWD_LEVELS } from "../../utils/constants";
import "./Dashboard.css";

const StationCard = ({ station }) => {
  const crowdLevel = station.current_crowd_level
    ? Math.round(station.current_crowd_level)
    : null;
  const crowdInfo = crowdLevel ? CROWD_LEVELS[crowdLevel] : null;

  return (
    <Link to={/stations/} className="station-card">
      <h4>{station.name}</h4>
      <p className="crowd-value">{station.line}</p>
      <div className="crowd-status">
        {crowdInfo ? (
          <>
            <span
              className="crowd-level"
              style={{ color: crowdInfo.color }}
            >
              {crowdInfo.label}
            </span>
            <span className="crowd-value">
              {station.current_crowd_level?.toFixed(1)} / 5
            </span>
          </>
        ) : (
          <span className="no-data">No recent reports</span>
        )}
      </div>
    </Link>
  );
};

export default StationCard;
