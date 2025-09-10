import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend
);

const CrowdChart = ({ stations }) => {
  if (!stations || stations.length === 0)
    return <p>No station data for chart</p>;

  const labels = stations.map((s) => s.name);
  const crowdLevels = stations.map((s) => s.current_crowd_level || 3);

  const data = {
    labels,
    datasets: [
      {
        label: "Current Crowd Levels",
        data: crowdLevels,
        borderColor: "#42a5f5",
        backgroundColor: "rgba(66, 165, 245, 0.2)",
        tension: 0.3,
        fill: true,
      },
    ],
  };

  return (
    <div>
      <h3>Crowd Levels Across Stations</h3>
      <Line data={data} />
    </div>
  );
};

export default CrowdChart;
