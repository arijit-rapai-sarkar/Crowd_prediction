import React, { useEffect, useState } from "react";
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
import stationService from "../../services/stations";
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

const TrendChart = () => {
  const [trend, setTrend] = useState(null);

  useEffect(() => {
    const fetchTrend = async () => {
      try {
        const overview = await stationService.getSystemOverview();
        const labels = Array.from({ length: 24 }, (_, index) => `${index}:00`);
        const base = overview.reports_last_24h || 0;
        const reports = labels.map((_, index) => {
          const modifier = 0.7 + 0.6 * Math.sin((index / 24) * Math.PI * 2);
          const noise = Math.random() * 0.3;
          return Math.round((base / 24) * (modifier + noise));
        });
        setTrend({ labels, reports });
      } catch (error) {
        console.error("Failed to build trend data", error);
      }
    };

    fetchTrend();
  }, []);

  if (!trend) {
    return <div className="loading">Loading trend data...</div>;
  }

  const data = {
    labels: trend.labels,
    datasets: [
      {
        label: "Estimated Reports",
        data: trend.reports,
        borderColor: CHART_COLORS.accent,
        backgroundColor: CHART_COLORS.accentBg,
        tension: 0.35,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: "top" },
      title: { display: false },
    },
  };

  return (
    <div style={{ height: "320px" }}>
      <Line data={data} options={options} />
    </div>
  );
};

export default TrendChart;


