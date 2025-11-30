import React, { useState } from 'react';
import axios from 'axios';

const ProductScanner = () => {
  // --- ESTADOS ---
  const [shoppingListId, setShoppingListId] = useState(null);
  const [barcode, setBarcode] = useState('');
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [msg, setMsg] = useState('');
  
  // Estados para los algoritmos nuevos
  const [alternative, setAlternative] = useState(null);
  const [optimizationResult, setOptimizationResult] = useState(null);

  const API_URL = 'http://127.0.0.1:8000/api';

  // 1. INICIAR LISTA
  const createShoppingList = async () => {
    setLoading(true);
    try {
      // Creamos lista con presupuesto de $10.000 para probar la optimización
      const response = await axios.post(`${API_URL}/lists/`, { budget_limit: 10000.00 });
      setShoppingListId(response.data.id);
      setMsg(`Lista #${response.data.id} creada con presupuesto $10.000`);
    } catch (err) { setError("Error creando lista"); } 
    finally { setLoading(false); }
  };

  // 2. ESCANEAR
  const handleScan = async (e) => {
    e.preventDefault();
    setLoading(true); setError(''); setProduct(null); setAlternative(null); setMsg('');
    try {
      const response = await axios.post(`${API_URL}/products/scan/`, { barcode });
      setProduct(response.data);
    } catch (err) { setError("Producto no encontrado o error de servidor"); } 
    finally { setLoading(false); }
  };

  // 3. AGREGAR A LISTA
  const handleAddToList = async () => {
    if (!product || !shoppingListId) return;
    try {
      await axios.post(`${API_URL}/lists/${shoppingListId}/add_item/`, {
        product_id: product.id, quantity: 1
      });
      setMsg(`✅ ${product.name} agregado a la lista.`);
    } catch (err) { setError("Error al agregar"); }
  };

  // 4. (NUEVO) ALGORITMO DE SUSTITUCIÓN
  const handleGetAlternative = async () => {
    if (!product) return;
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/products/${product.id}/alternative/`);
      if (response.data.found) {
        setAlternative(response.data); // Guardamos la sugerencia
      } else {
        alert("No se encontraron alternativas mejores para este producto.");
      }
    } catch (err) { setError("Error buscando alternativa"); }
    finally { setLoading(false); }
  };

  // 5. (NUEVO) ALGORITMO DE MOCHILA (OPTIMIZACIÓN)
  const handleOptimize = async () => {
    if (!shoppingListId) return;
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/lists/${shoppingListId}/optimize/`);
      setOptimizationResult(response.data);
    } catch (err) { setError("Error optimizando lista"); }
    finally { setLoading(false); }
  };

  // --- VISTA ---
  return (
    <div style={{ maxWidth: '600px', margin: '20px auto', fontFamily: 'Arial', textAlign: 'center', padding: '20px' }}>
      <h1>🛒 Liquiverde MVP</h1>

      {/* PASO 1: CREAR LISTA */}
      {!shoppingListId && (
        <button onClick={createShoppingList} style={styles.btnBig}>
          🚀 Iniciar Nueva Compra
        </button>
      )}

      {/* PASO 2: ESCÁNER */}
      {shoppingListId && (
        <div>
          <div style={{background: '#e3f2fd', padding: '10px', borderRadius: '5px', marginBottom: '20px'}}>
            <strong>Lista Activa #{shoppingListId}</strong> | Presupuesto: $10.000
          </div>

          <form onSubmit={handleScan}>
            <input 
              value={barcode} onChange={(e) => setBarcode(e.target.value)}
              placeholder="Ej. 750100..." style={styles.input}
            />
            <button type="submit" disabled={loading} style={styles.btnScan}>🔍 Escanear</button>
          </form>

          {/* TARJETA DE PRODUCTO */}
          {product && (
            <div style={styles.card}>
              <h3>{product.name}</h3>
              <p>Precio: ${product.price}</p>
              <p>CO2: {product.carbon_footprint} kg</p>
              <p>Eco-Score: <strong>{product.sustainability_score.grade || product.sustainability_score}</strong></p>

              <div style={{display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '10px'}}>
                <button onClick={handleAddToList} style={styles.btnAdd}>➕ Agregar</button>
                <button onClick={handleGetAlternative} style={styles.btnAlt}>♻️ Buscar Alternativa</button>
              </div>

              {/* RESULTADO SUSTITUCIÓN */}
              {alternative && (
                <div style={{marginTop: '15px', padding: '10px', background: '#dcedc8', borderRadius: '5px', border: '1px solid #8bc34a'}}>
                  <strong>¡Sugerencia Ecológica! 💡</strong>
                  <p>Cambia por: <b>{alternative.name}</b></p>
                  <p>{alternative.reason}</p>
                </div>
              )}
            </div>
          )}

          {/* PASO 3: OPTIMIZAR */}
          <hr style={{margin: '30px 0'}} />
          <button onClick={handleOptimize} style={styles.btnOpt}>⚡ Optimizar Mi Lista (Knapsack)</button>

          {/* RESULTADO OPTIMIZACIÓN */}
          {optimizationResult && (
            <div style={{marginTop: '20px', padding: '20px', background: '#fff3e0', borderRadius: '8px', border: '1px solid #ffb74d'}}>
              <h3>📊 Resultado Optimización</h3>
              <p>El algoritmo seleccionó los mejores productos para tu presupuesto:</p>
              <ul style={{textAlign: 'left'}}>
                {optimizationResult.optimized_items.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
              <p><strong>Costo Total:</strong> ${optimizationResult.total_cost}</p>
              <p><strong>Ahorro Estimado:</strong> ${optimizationResult.total_savings}</p>
            </div>
          )}
        </div>
      )}
      
      {msg && <p style={{color: 'green', fontWeight: 'bold'}}>{msg}</p>}
      {error && <p style={{color: 'red'}}>{error}</p>}
    </div>
  );
};

const styles = {
  input: { padding: '10px', fontSize: '16px', width: '60%' },
  card: { border: '1px solid #ccc', padding: '20px', margin: '20px 0', borderRadius: '8px' },
  btnBig: { padding: '15px 30px', fontSize: '18px', background: '#2196f3', color: 'white', border: 'none', cursor: 'pointer', borderRadius: '5px' },
  btnScan: { padding: '10px 20px', marginLeft: '10px', background: '#607d8b', color: 'white', border: 'none', cursor: 'pointer' },
  btnAdd: { padding: '10px', background: '#4caf50', color: 'white', border: 'none', cursor: 'pointer', borderRadius: '5px' },
  btnAlt: { padding: '10px', background: '#ff9800', color: 'white', border: 'none', cursor: 'pointer', borderRadius: '5px' },
  btnOpt: { padding: '15px', width: '100%', background: '#673ab7', color: 'white', border: 'none', cursor: 'pointer', fontSize: '16px', borderRadius: '5px' }
};

export default ProductScanner;