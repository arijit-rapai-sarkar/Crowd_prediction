import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import stationService from "../../services/stations";
import { CROWD_LEVELS } from "../../utils/constants";
import "./Stations.css";

const StationList = () => {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");
  const navigate = useNavigate();

  useEffect(() => {
    fetchStations();
  }, []);

  const fetchStations = async () => {
    try {
      setLoading(true);
      const data = await stationService.getAll();
      setStations(data);
    } catch (error) {
      console.error("Error fetching stations", error);
    } finally {
      setLoading(false);
    }
  };

  const filteredStations = stations.filter((station) => {
    if (filter === "all") return true;
    return station.station_type === filter;
  });

  if (loading) {
    return <div className="loading">Loading stations...</div>;
  }

  return (
    <div className="station-list">
      <div className="list-header">
        <h2>All Stations</h2>
        <div className="filter-buttons">
          {[
            ["all", "All"],
            ["metro", "Metro"],
            ["bus", "Bus"],
            ["train", "Train"],
          ].map(([value, label]) => (
            <button
              key={value}
              className={filter === value ? "active" : ""}
              onClick={() => setFilter(value)}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="stations-table">
        <table>
          <thead>
            <tr>
              <th>Station Name</th>
              <th>Line</th>
              <th>Type</th>
              <th>Current Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredStations.map((station) => {
              const crowdLevel = station.current_crowd_level
                ? Math.round(station.current_crowd_level)
                : null;
              const crowdInfo =
                crowdLevel && CROWD_LEVELS[crowdLevel]
                  ? CROWD_LEVELS[crowdLevel]
                  : null;

              return (
                <tr key={station.id}>
                  <td>{station.name}</td>
                  <td>{station.line}</td>
                  <td>
                    <span className={`type-badge ${station.station_type}`}>
                      {station.station_type}
                    </span>
                  </td>
                  <td>
                    {crowdInfo ? (
                      <span
                        className="crowd-badge"
                        style={{
                          backgroundColor: `${crowdInfo.color}20`,
                          color: crowdInfo.color,
                        }}
                      >
                        {crowdInfo.label}
                      </span>
                    ) : (
                      <span className="no-data">No data</span>
                    )}
                  </td>
                  <td>
                    <button
                      className="view-btn"
                      onClick={() => navigate(`/stations/${station.id}`)}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default StationList;
