import React, { useState } from 'react';
import { productService } from '../services/api';

const ProductScanner = () => {
  // Estados
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // ID de la lista DEMO (la misma que usas en el optimizador)
  const LIST_ID = 1;

  // 1. Función para BUSCAR el producto
  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const res = await productService.scan(query);
      if (res.data) {
        setResult(res.data);
      } else {
        setError('No se encontraron datos.');
      }
    } catch (err) {
      setError('Producto no encontrado o error de conexión.');
    } finally {
      setLoading(false);
    }
  };

  // 2. Función para AGREGAR a la lista (Backend real)
  const handleAddToList = async () => {
    // Validación de seguridad
    if (!result || !result.id) {
        alert("Error: Este producto no tiene ID local. Asegúrate de haber ejecutado seed_db.");
        return;
    }

    try {
        // Llamada al endpoint que creamos en el paso anterior
        await productService.addItem(LIST_ID, result.id, 1);
        
        alert(`✅ ¡${result.name} agregado correctamente!`);
        
        // Limpiamos para una nueva búsqueda
        setResult(null);
        setQuery('');
    } catch (err) {
        console.error(err);
        alert("❌ Error al guardar. Revisa la consola.");
    }
  };

  return (
    <div className="page-content scanner-page">
      <h1>🔍 Escáner de Productos</h1>
      <p>Ingresa un código de barras o nombre (ej: "Leche", "Carne", "780123456004")</p>

      {/* Formulario de Búsqueda */}
      <form onSubmit={handleSearch} className="search-box">
        <input 
          type="text" 
          placeholder="Escribe aquí..." 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Buscando...' : 'Buscar'}
        </button>
      </form>

      {/* Mensaje de Error */}
      {error && <div className="error-msg">{error}</div>}

      {/* Tarjeta de Resultados */}
      {result && (
        <div className="card product-result fadeIn">
          <div className="result-header">
            <img 
                src={result.image_url || 'https://via.placeholder.com/150'} 
                alt={result.name} 
                className="result-img"
            />
            <div>
              <h2>{result.name}</h2>
              <span className="brand">{result.brand || 'Marca Genérica'}</span>
            </div>
          </div>
          
          <div className="result-stats">
            <div className="stat">
              <label>Precio Est.</label>
              <span>${parseInt(result.price).toLocaleString()}</span>
            </div>
            <div className="stat">
              <label>Huella CO2</label>
              <span>{result.carbon_footprint} kg</span>
            </div>
            <div className="stat">
              <label>Score</label>
              <span className={`grade grade-${result.sustainability_grade?.toLowerCase()}`}>
                {result.sustainability_grade || 'C'}
              </span>
            </div>
          </div>
          
          {/* Botón de Acción Real */}
          <div className="scanner-actions">
            <button className="btn-secondary" onClick={handleAddToList}>
                ➕ Agregar a Lista Actual
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProductScanner;