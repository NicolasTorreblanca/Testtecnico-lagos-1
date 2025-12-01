import React from 'react';

const KpiCard = ({ title, value, subtext, colorClass, icon }) => {
  return (
    <div className={`kpi-card ${colorClass}`}>
      <div className="kpi-icon">{icon}</div>
      <div className="kpi-content">
        <h3>{title}</h3>
        <div className="big-number">{value}</div>
        {subtext && <p className="subtext">{subtext}</p>}
      </div>
    </div>
  );
};

export default KpiCard;