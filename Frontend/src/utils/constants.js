// Shared constants for crowd level semantics and visual styling

export const CROWD_LEVELS = {
  1: {
    label: "Empty",
    description: "Very few riders; plenty of open space",
    color: "#16a34a",
  },
  2: {
    label: "Light",
    description: "Comfortable load with many seats available",
    color: "#22c55e",
  },
  3: {
    label: "Moderate",
    description: "Standing room beginning to fill up",
    color: "#facc15",
  },
  4: {
    label: "Busy",
    description: "Crowded but moving; limited personal space",
    color: "#fb923c",
  },
  5: {
    label: "Crowded",
    description: "Very crowded; expect delays and limited movement",
    color: "#ef4444",
  },
};

export const CHART_COLORS = {
  primary: "#6366f1",
  primaryBg: "rgba(99, 102, 241, 0.15)",
  accent: "#22d3ee",
  accentBg: "rgba(34, 211, 238, 0.2)",
};

export const DEFAULT_MAP_CENTER = [40.7128, -74.006];
