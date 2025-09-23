import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { CHART_COLORS } from "../../utils/constants";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const CrowdChart = ({ stations = [] }) => {
  if (!stations.length) {
    return <p className="no-data">No station data available</p>;
  }

  const labels = stations.map((station) => station.name);
  const crowdLevels = stations.map((station) =>
    station.current_crowd_level ? Number(station.current_crowd_level.toFixed(2)) : 0
  );

  const data = {
    labels,
    datasets: [
      {
        label: "Current Crowd Level",
        data: crowdLevels,
        borderColor: CHART_COLORS.primary,
        backgroundColor: CHART_COLORS.primaryBg,
        fill: true,
        tension: 0.35,
        pointRadius: 3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" },
      title: { display: false },
      tooltip: {
        callbacks: {
          label: (context) => `${context.raw} / 5`,
        },
      },
    },
    scales: {
      y: {
        min: 0,
        max: 5,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div style={{ height: "320px" }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default CrowdChart;

