import API from "./api";

// Get all stations
export const getStations = async () => {
  const response = await API.get("/stations");
  return response.data;
};

// Get single station by ID
export const getStation = async (id) => {
  const response = await API.get(`/stations/${id}`);
  return response.data;
};

// Submit a crowd report
export const submitCrowdReport = async (data) => {
  const response = await API.post("/crowd-reports", data);
  return response.data;
};

// Get predictions for a station
export const getStationPredictions = async (id) => {
  const response = await API.get(`/predictions/station/${id}`);
  return response.data;
};

// Get hourly predictions for a station
export const getHourlyPredictions = async (id, hours = 24) => {
  const response = await API.get(`/predictions/hourly/${id}?hours=${hours}`);
  return response.data;
};

// Get station-level analytics
export const getStationAnalytics = async (id) => {
  const response = await API.get(`/analytics/station/${id}`);
  return response.data;
};

// Get system-wide analytics
export const getSystemAnalytics = async () => {
  const response = await API.get("/analytics/system");
  return response.data;
};
