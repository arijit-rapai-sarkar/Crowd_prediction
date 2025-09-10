import API from "./api";

// Login user
export const login = async (credentials) => {
  const response = await API.post("/auth/login", credentials);
  return response.data;
};

// Register user
export const register = async (data) => {
  const response = await API.post("/auth/register", data);
  return response.data;
};
