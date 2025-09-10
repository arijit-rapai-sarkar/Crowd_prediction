import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Layout from './components/Layout/Layout';
import Dashboard from './components/Dashboard/Dashboard';
import StationList from './components/Stations/StationList';
import StationDetail from './components/Stations/StationDetail';
import Analytics from './components/Analytics/Analytics';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="stations" element={<StationList />} />
            <Route path="stations/:id" element={<StationDetail />} />
            <Route path="analytics" element={<Analytics />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
