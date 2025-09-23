import API from "./api";

const stationService = {
  async getAll(params = {}) {
    const response = await API.get("/stations", { params });
    return response.data;
  },

  async getById(id) {
    const response = await API.get(`/stations/${id}`);
    return response.data;
  },

  async getStationReports(id, hours = 24) {
    const response = await API.get(`/crowd-reports/station/${id}`, {
      params: { hours },
    });
    return response.data;
  },

  async createCrowdReport(id, crowdLevel, description) {
    const payload = {
      station_id: Number(id),
      crowd_level: crowdLevel,
      description,
    };
    const response = await API.post("/crowd-reports", payload);
    return response.data;
  },

  async getHourlyPredictions(id, hours = 24) {
    const response = await API.get(`/predictions/hourly/${id}`, {
      params: { hours },
    });
    return response.data;
  },

  async getStationPredictions(id, limit = 10) {
    const response = await API.get(`/predictions/station/${id}`, {
      params: { limit },
    });
    return response.data;
  },

  async requestPrediction(stationId, hoursAhead = 1) {
    const response = await API.post("/predictions/predict", {
      station_id: Number(stationId),
      hours_ahead: hoursAhead,
    });
    return response.data;
  },

  async getStationAnalytics(id, days = 7) {
    const response = await API.get(`/analytics/station/${id}`, {
      params: { days },
    });
    return response.data;
  },

  async getSystemOverview() {
    const response = await API.get("/analytics/overview");
    return response.data;
  },
};

export { stationService };
export default stationService;
