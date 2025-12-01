import React, { useState, useEffect } from 'react';
import { productService } from '../services/api';
import ProductCard from '../Components/ProductCard';
import OptimizationControls from '../Components/OptimizationControls';

const ShoppingListOptimizer = () => {
  // Estado
  const [items, setItems] = useState([]);
  const [budget, setBudget] = useState(20000);
  const [weightPrice, setWeightPrice] = useState(0.5);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);

  // ID fijo para la demo (creado por seed_db)
  const LIST_ID = 1; 

  // Cargar lista al iniciar
  useEffect(() => {
    loadList();
  }, []);

  const loadList = async () => {
    try {
      const res = await productService.getList(LIST_ID);
      setItems(res.data.items);
      updateStats(res.data);
    } catch (err) {
      console.error("Error cargando lista", err);
    }
  };

  const updateStats = (data) => {
    setStats({
      total: data.total_price || 0,
      savings: data.total_savings || 0,
      score: data.sustainability_grade || 'C'
    });
  };

  const handleOptimize = async () => {
    setLoading(true);
    try {
      // Preparamos los datos para el algoritmo Multi-objetivo [cite: 59]
      const payload = {
        shopping_list_id: LIST_ID,
        budget_limit: budget,
        importance_price: weightPrice,
        importance_sustainability: 1 - weightPrice, // El complemento es para el planeta
        allow_substitutions: true // Requisito: Algoritmo de sustitución [cite: 61]
      };
      
      const res = await productService.optimize(LIST_ID, payload);
      
      // Actualizamos la vista con la respuesta del algoritmo
      setItems(res.data.items);
      updateStats(res.data);
      
    } catch (err) {
      alert("Error ejecutando optimización. Asegúrate de que el Backend esté corriendo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page-content">
      <header className="page-header">
        <h1>🛒 Optimizador de Compras</h1>
        <p>Ajusta tu presupuesto y preferencias para obtener la mejor lista.</p>
      </header>

      <div className="optimizer-grid">
        {/* Panel Izquierdo: Controles */}
        <div className="left-panel">
          <OptimizationControls 
            budget={budget} setBudget={setBudget}
            weightPrice={weightPrice} setWeightPrice={setWeightPrice}
            onOptimize={handleOptimize}
            loading={loading}
          />
          
          {/* Resumen Rápido */}
          {stats && (
            <div className="card summary-card">
              <h3>Resumen Actual</h3>
              <div className="summary-row">
                <span>Total a Pagar:</span>
                <strong className="price-text">${parseInt(stats.total).toLocaleString()}</strong>
              </div>
              <div className="summary-row savings">
                <span>Ahorro Detectado:</span>
                <strong>${parseInt(stats.savings).toLocaleString()}</strong>
              </div>
              <div className="summary-row">
                 <span>Nivel Eco:</span>
                 <span className={`grade-badge grade-${stats.score.toLowerCase()}`}>{stats.score}</span>
              </div>
            </div>
          )}
        </div>

        {/* Panel Derecho: Lista de Productos */}
        <div className="right-panel">
          <h3>Tu Lista ({items.length} productos)</h3>
          <div className="products-container">
            {items.map(item => (
              <ProductCard key={item.id} item={item} />
            ))}
            {items.length === 0 && <p className="empty-msg">Cargando productos...</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShoppingListOptimizer;