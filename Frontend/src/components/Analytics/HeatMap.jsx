import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip } from "react-leaflet";
import stationService from "../../services/stations";
import { CROWD_LEVELS, DEFAULT_MAP_CENTER } from "../../utils/constants";
import "leaflet/dist/leaflet.css";

const HeatMap = () => {
  const [stations, setStations] = useState([]);

  useEffect(() => {
    const fetchStations = async () => {
      try {
        const data = await stationService.getAll();
        setStations(data);
      } catch (error) {
        console.error("Failed to fetch stations for heatmap", error);
      }
    };

    fetchStations();
  }, []);

  return (
    <MapContainer
      center={DEFAULT_MAP_CENTER}
      zoom={12}
      style={{ height: "400px", width: "100%" }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />

      {stations.map((station) => {
        const crowdLevel = station.current_crowd_level
          ? Math.round(station.current_crowd_level)
          : 3;
        const levelInfo = CROWD_LEVELS[crowdLevel];

        return (
          <CircleMarker
            key={station.id}
            center={[station.latitude, station.longitude]}
            radius={8 + crowdLevel}
            fillOpacity={0.6}
            color={levelInfo.color}
          >
            <Tooltip direction="top" offset={[0, -4]}>
              <strong>{station.name}</strong>
              <br />
              Line: {station.line}
              <br />
              Status: {levelInfo.label}
            </Tooltip>
          </CircleMarker>
        );
      })}
    </MapContainer>
  );
};

export default HeatMap;
