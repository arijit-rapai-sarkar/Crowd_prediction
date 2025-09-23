import React, { useState } from "react";
import { CROWD_LEVELS } from "../../utils/constants";
import "./Stations.css";

const CrowdReportForm = ({ onSubmit, onClose }) => {
  const [crowdLevel, setCrowdLevel] = useState(3);
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      setSubmitting(true);
      await onSubmit(crowdLevel, description.trim());
      setDescription("");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h3>Report Current Crowd Level</h3>
          <button className="close-btn" onClick={onClose} aria-label="Close">
            X
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Crowd Level</label>
            <div className="crowd-level-selector">
              {Object.entries(CROWD_LEVELS).map(([level, info]) => {
                const isSelected = Number(level) === crowdLevel;
                return (
                  <button
                    key={level}
                    type="button"
                    className={`level-btn ${isSelected ? "selected" : ""}`}
                    style={{
                      backgroundColor: isSelected ? info.color : "white",
                      color: isSelected ? "white" : info.color,
                      borderColor: info.color,
                    }}
                    onClick={() => setCrowdLevel(Number(level))}
                  >
                    {info.label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="form-group">
            <label>Description (optional)</label>
            <textarea
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Share crowd observations, delays, or other notes"
              rows={3}
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="cancel-btn"
              onClick={onClose}
              disabled={submitting}
            >
              Cancel
            </button>
            <button type="submit" className="submit-btn" disabled={submitting}>
              {submitting ? "Submitting..." : "Submit Report"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CrowdReportForm;
