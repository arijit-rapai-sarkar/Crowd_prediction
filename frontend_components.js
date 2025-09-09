// frontend/src/components/Dashboard/Dashboard.css
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard h2 {
  margin-bottom: 2rem;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stat-card h3 {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}

.stations-section h3,
.chart-section h3 {
  margin-bottom: 1rem;
  color: #333;
}

.stations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.station-card {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #ccc;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.station-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.station-card h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.station-line {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.crowd-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.crowd-level {
  font-weight: bold;
}

.crowd-value {
  color: #666;
  font-size: 0.9rem;
}

.no-data {
  color: #999;
  font-style: italic;
}

// frontend/src/components/Stations/StationList.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { stationService } from '../../services/stations';
import { CROWD_LEVELS } from '../../utils/constants';
import './Stations.css';

function StationList() {
  const [stations, setStations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
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
      console.error('Error fetching stations:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredStations = stations.filter(station => {
    if (filter === 'all') return true;
    return station.station_type === filter;
  });

  if (loading) return <div className="loading">Loading stations...</div>;

  return (
    <div className="station-list">
      <div className="list-header">
        <h2>All Stations</h2>
        <div className="filter-buttons">
          <button 
            className={filter === 'all' ? 'active' : ''}
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button 
            className={filter === 'metro' ? 'active' : ''}
            onClick={() => setFilter('metro')}
          >
            Metro
          </button>
          <button 
            className={filter === 'bus' ? 'active' : ''}
            onClick={() => setFilter('bus')}
          >
            Bus
          </button>
          <button 
            className={filter === 'train' ? 'active' : ''}
            onClick={() => setFilter('train')}
          >
            Train
          </button>
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
            {filteredStations.map(station => {
              const crowdLevel = station.current_crowd_level ? 
                Math.round(station.current_crowd_level) : null;
              const crowdInfo = crowdLevel ? CROWD_LEVELS[crowdLevel] : null;
              
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
                        style={{ backgroundColor: crowdInfo.color + '20', 
                                color: crowdInfo.color }}
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
}

export default StationList;

// frontend/src/components/Stations/StationDetail.js
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Line } from 'react-chartjs-2';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { stationService } from '../../services/stations';
import CrowdReportForm from './CrowdReportForm';
import { CROWD_LEVELS, CHART_COLORS } from '../../utils/constants';
import './Stations.css';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png'
});

function StationDetail() {
  const { id } = useParams();
  const [station, setStation] = useState(null);
  const [reports, setReports] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showReportForm, setShowReportForm] = useState(false);

  useEffect(() => {
    fetchStationData();
  }, [id]);

  const fetchStationData = async () => {
    try {
      setLoading(true);
      const [stationData, reportsData, predictionsData, analyticsData] = await Promise.all([
        stationService.getById(id),
        stationService.getStationReports(id, 24),
        stationService.getHourlyPredictions(id, 24),
        stationService.getStationAnalytics(id, 7)
      ]);
      
      setStation(stationData);
      setReports(reportsData);
      setPredictions(predictionsData.predictions);
      setAnalytics(analyticsData);
    } catch (error) {
      console.error('Error fetching station data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleReportSubmit = async (crowdLevel, description) => {
    try {
      await stationService.createCrowdReport(id, crowdLevel, description);
      setShowReportForm(false);
      fetchStationData(); // Refresh data
    } catch (error) {
      console.error('Error submitting report:', error);
    }
  };

  if (loading) return <div className="loading">Loading station details...</div>;
  if (!station) return <div className="error">Station not found</div>;

  // Prepare chart data
  const chartData = {
    labels: predictions.map(p => new Date(p.time).toLocaleTimeString([], { hour: '2-digit' })),
    datasets: [
      {
        label: 'Predicted Crowd Level',
        data: predictions.map(p => p.predicted_crowd_level),
        borderColor: CHART_COLORS.primary,
        backgroundColor: CHART_COLORS.primaryBg,
        tension: 0.4
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: '24-Hour Crowd Prediction'
      }
    },
    scales: {
      y: {
        min: 0,
        max: 5,
        ticks: {
          stepSize: 1
        }
      }
    }
  };

  const crowdLevel = station.current_crowd_level ? Math.round(station.current_crowd_level) : null;
  const crowdInfo = crowdLevel ? CROWD_LEVELS[crowdLevel] : null;

  return (
    <div className="station-detail">
      <div className="detail-header">
        <div>
          <h2>{station.name}</h2>
          <p className="station-meta">
            {station.line} • {station.station_type}
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
          {analytics && (
            <div className="analytics-stats">
              <div className="stat">
                <span className="stat-label">Total Reports:</span>
                <span className="stat-value">{analytics.total_reports}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Avg Crowd:</span>
                <span className="stat-value">{analytics.average_crowd_level}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Peak Hours:</span>
                <span className="stat-value">
                  {analytics.peak_hours.length > 0 ? 
                    analytics.peak_hours.join(', ') : 'N/A'}
                </span>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="chart-container">
        <Line data={chartData} options={chartOptions} />
      </div>

      <div className="map-section">
        <h3>Station Location</h3>
        <div className="map-container">
          <MapContainer 
            center={[station.latitude, station.longitude]} 
            zoom={15} 
            style={{ height: '300px', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; OpenStreetMap contributors'
            />
            <Marker position={[station.latitude, station.longitude]}>
              <Popup>
                {station.name}<br />
                {station.line}
              </Popup>
            </Marker>
          </MapContainer>
        </div>
      </div>

      <div className="recent-reports">
        <h3>Recent Reports</h3>
        {reports.length > 0 ? (
          <div className="reports-list">
            {reports.slice(0, 5).map(report => (
              <div key={report.id} className="report-item">
                <div className="report-level">
                  <span 
                    className="level-badge"
                    style={{ backgroundColor: CROWD_LEVELS[report.crowd_level].color + '20',
                            color: CROWD_LEVELS[report.crowd_level].color }}
                  >
                    {CROWD_LEVELS[report.crowd_level].label}
                  </span>
                </div>
                <div className="report-details">
                  {report.description && <p>{report.description}</p>}
                  <span className="report-time">
                    {new Date(report.created_at).toLocaleString()}
                  </span>
                </div>
              </div>
            ))}
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
}

export default StationDetail;