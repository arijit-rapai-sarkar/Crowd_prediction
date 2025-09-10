import React, { useState } from "react";
import { submitCrowdReport } from "../../services/stations";
import "./Stations.css";

const CrowdReportForm = ({ stationId, onClose }) => {
  const [crowdLevel, setCrowdLevel] = useState(3);
  const [message, setMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await submitCrowdReport({ station_id: stationId, crowd_level: crowdLevel });
      setMessage("Report submitted successfully!");
      setTimeout(onClose, 1500);
    } catch (error) {
      console.error("Failed to submit crowd report", error);
      setMessage("Failed to submit report.");
    }
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h3>Submit Crowd Report</h3>
        <form onSubmit={handleSubmit}>
          <label>
            Crowd Level:
            <select
              value={crowdLevel}
              onChange={(e) => setCrowdLevel(parseInt(e.target.value))}
            >
              <option value={1}>Empty</option>
              <option value={2}>Light</option>
              <option value={3}>Moderate</option>
              <option value={4}>Busy</option>
              <option value={5}>Crowded</option>
            </select>
          </label>
          <button type="submit">Submit</button>
          <button type="button" onClick={onClose} className="cancel-btn">
            Cancel
          </button>
        </form>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
};

export default CrowdReportForm;
