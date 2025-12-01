import React from 'react';

const OptimizationControls = ({ budget, setBudget, weightPrice, setWeightPrice, onOptimize, loading }) => {
  return (
    <div className="card control-panel">
      <h2>⚙️ Configuración del Algoritmo</h2>
      
      <div className="controls-grid">
        <div className="input-group">
            <label>💰 Presupuesto Máximo</label>
            <input 
              type="number" 
              value={budget} 
              onChange={(e) => setBudget(Number(e.target.value))}
              className="input-field"
            />
        </div>

        <div className="input-group">
            <label>⚖️ Balance: Ahorro vs. Planeta</label>
            <input 
              type="range" 
              min="0" max="1" step="0.1" 
              value={weightPrice}
              onChange={(e) => setWeightPrice(Number(e.target.value))}
              className="range-input"
            />
            <div className="range-labels">
              <span>🌍 100% Eco</span>
              <span>Neutral</span>
              <span>100% Ahorro 💰</span>
            </div>
        </div>
      </div>

      <button onClick={onOptimize} disabled={loading} className="btn-primary">
        {loading ? '🔄 Ejecutando Algoritmo...' : '🚀 Optimizar Mi Lista'}
      </button>
    </div>
  );
};

export default OptimizationControls;