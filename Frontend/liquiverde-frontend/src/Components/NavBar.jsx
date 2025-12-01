import React from 'react';
import { Link, useLocation } from 'react-router-dom';
//import './NavBar.css'; // Crearemos este CSS al final

const NavBar = () => {
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        🌱 LiquiVerde
      </div>
      <div className="navbar-links">
        <Link to="/" className={`nav-link ${isActive('/')}`}>
          🛒 Optimizador
        </Link>
        <Link to="/scanner" className={`nav-link ${isActive('/scanner')}`}>
          🔍 Escáner
        </Link>
        <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
          📊 Impacto
        </Link>
      </div>
    </nav>
  );
};

export default NavBar;