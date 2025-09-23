import React from "react";
import { NavLink } from "react-router-dom";
import "./Layout.css";

const Sidebar = () => {
  return (
    <aside className="sidebar">
      <nav>
        <ul>
          <li>
            <NavLink to="/" end>
              Dashboard
            </NavLink>
          </li>
          <li>
            <NavLink to="/stations">Stations</NavLink>
          </li>
          <li>
            <NavLink to="/analytics">Analytics</NavLink>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
