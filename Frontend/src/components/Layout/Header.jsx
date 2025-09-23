import React, { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";
import "./Layout.css";

const Header = () => {
  const { user, logout, isAuthenticated } = useContext(AuthContext);

  return (
    <header className="header">
      <h1 className="header-title">Crowding Predictor</h1>
      <div className="header-user">
        {isAuthenticated ? (
          <>
            <span>Welcome, {user.username}</span>
            <button onClick={logout}>Logout</button>
          </>
        ) : (
          <span>Guest</span>
        )}
      </div>
    </header>
  );
};

export default Header;
