import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { getSystemAnalytics } from "../../services/stations";
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

const TrendChart = () => {
  const [trendData, setTrendData] = useState(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await getSystemAnalytics();
        // Example: build fake hourly trend from reports count
        const labels = Array.from({ length: 24 }, (_, i) => `${i}:00`);
        const reports = labels.map(
          (_, i) => Math.floor((data.total_reports / 24) * (Math.random() + 0.5))
        );
        setTrendData({ labels, reports });
      } catch (error) {
        console.error("Failed to fetch trend data", error);
      }
    };
    fetchAnalytics();
  }, []);

  if (!trendData) return <div className="loading">Loading trend chart...</div>;

  const chartData = {
    labels: trendData.labels,
    datasets: [
      {
        label: "Reports (approx)",
        data: trendData.reports,
        fill: false,
        borderColor: "#42a5f5",
        tension: 0.2,
      },
    ],
  };

  return <Line data={chartData} />;
};

export default TrendChart;
