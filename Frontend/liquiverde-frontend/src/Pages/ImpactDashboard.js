import React, { useEffect, useState } from 'react';
import { productService } from '../services/api';
import KpiCard from '../Components/KpiCard';

const ImpactDashboard = () => {
  const [metrics, setMetrics] = useState({ co2: 0, savings: 0, score: 'B' });

  useEffect(() => {
    // Obtenemos datos de la lista base para proyectar impacto
    productService.getList(1).then(res => {
      setMetrics({
        co2: res.data.total_co2_impact || 5.2,
        savings: res.data.total_savings || 0,
        score: res.data.sustainability_grade || 'B'
      });
    }).catch(err => console.log("Usando datos default..."));
  }, []);

  return (
    <div className="page-content">
      <header className="page-header">
        <h1>📊 Tu Impacto Ambiental</h1>
        <p>Resumen de tus hábitos de consumo sostenible.</p>
      </header>

      <div className="kpi-grid">
        <KpiCard 
          title="CO2 Evitado (Estimado)" 
          value={`${(metrics.co2 * 0.5).toFixed(1)} kg`} 
          subtext="Equivale a cargar 500 celulares 📱"
          colorClass="green"
          icon="🌳"
        />
        <KpiCard 
          title="Dinero Ahorrado" 
          value={`$${parseInt(metrics.savings).toLocaleString()}`} 
          subtext="En tu última lista optimizada"
          colorClass="blue"
          icon="💰"
        />
        <KpiCard 
          title="Nivel Eco-Shopper" 
          value={metrics.score} 
          subtext="Basado en tus elecciones recientes"
          colorClass="teal"
          icon="⭐"
        />
      </div>

      <div className="card chart-placeholder">
        <h3>Historial de Huella de Carbono (Mensual)</h3>
        {/* Placeholder visual para gráfico */}
        <div className="fake-chart">
            <div className="bar" style={{height: '40%'}} title="Ene"></div>
            <div className="bar" style={{height: '60%'}} title="Feb"></div>
            <div className="bar" style={{height: '35%'}} title="Mar"></div>
            <div className="bar" style={{height: '80%'}} title="Abr"></div>
            <div className="bar active" style={{height: '50%'}} title="May"></div>
        </div>
        <p style={{textAlign:'center', color:'#888', marginTop:'10px'}}>
            Comparativa de tus últimos 5 meses de consumo.
        </p>
      </div>
    </div>
  );
};

export default ImpactDashboard;