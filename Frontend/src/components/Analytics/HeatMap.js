import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import { getStations } from "../../services/stations";
import { CROWD_COLORS, CROWD_LEVELS } from "../../utils/constants";
import "leaflet/dist/leaflet.css";

const HeatMap = () => {
  const [stations, setStations] = useState([]);

  useEffect(() => {
    const fetchStations = async () => {
      try {
        const data = await getStations();
        setStations(data);
      } catch (error) {
        console.error("Failed to fetch stations for heatmap", error);
      }
    };
    fetchStations();
  }, []);

  return (
    <MapContainer
      center={[28.6139, 77.209]} // default center (Delhi as placeholder)
      zoom={11}
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="© OpenStreetMap contributors"
      />

      {stations.map((station) => (
        <CircleMarker
          key={station.id}
          center={[station.latitude, station.longitude]}
          radius={10}
          fillOpacity={0.7}
          color={CROWD_COLORS[station.current_crowd_level || 3]}
        >
          <Tooltip>
            <strong>{station.name}</strong>
            <br />
            Current: {CROWD_LEVELS[station.current_crowd_level || 3]}
          </Tooltip>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};

export default HeatMap;
