import React, { createContext, useState, useEffect } from "react";
import { login as loginUser, register as registerUser } from "../services/auth";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  // If token exists on reload, keep user logged in
  useEffect(() => {
    if (token) {
      setUser({ username: localStorage.getItem("username") });
    }
  }, [token]);

  // Handle login
  const login = async (credentials) => {
    try {
      const response = await loginUser(credentials);
      setToken(response.access_token);
      localStorage.setItem("token", response.access_token);
      localStorage.setItem("username", credentials.username);
      setUser({ username: credentials.username });
      return true;
    } catch (error) {
      console.error("Login failed", error);
      return false;
    }
  };

  // Handle register
  const register = async (data) => {
    try {
      const response = await registerUser(data);
      return response;
    } catch (error) {
      console.error("Registration failed", error);
      throw error;
    }
  };

  // Handle logout
  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("username");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
