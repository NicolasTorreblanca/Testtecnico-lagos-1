import React from 'react';

const ProductCard = ({ item }) => {
  const { product, is_suggested_alternative, quantity, substitution_details } = item;
  
  // Definir color del score (A=Verde, E=Rojo)
  const getScoreColor = (grade) => {
    const map = { 'A': '#27ae60', 'B': '#2ecc71', 'C': '#f1c40f', 'D': '#e67e22', 'E': '#e74c3c' };
    return map[grade] || '#95a5a6';
  };

  return (
    <div className={`product-card ${is_suggested_alternative ? 'substituted' : ''}`}>
      <div className="product-image">
        {/* Placeholder si no hay imagen real */}
        <div className="img-placeholder">{product.name.charAt(0)}</div>
      </div>
      
      <div className="product-details">
        <div className="header-row">
            <h3>{product.name}</h3>
            {is_suggested_alternative && (
                <span className="badge-sub">✨ Recomendación Eco-Smart</span>
            )}
        </div>
        <p className="category">{product.category} • {product.brand}</p>
        
        {/* Detalles de sustitución (Bonus) */}
        {is_suggested_alternative && substitution_details && (
             <div className="sub-reason">
                💡 <strong>Motivo:</strong> {substitution_details.reason}
             </div>
        )}
      </div>

      <div className="product-metrics">
        <div className="price-tag">${parseInt(product.price).toLocaleString()}</div>
        <div className="eco-badge" style={{ borderColor: getScoreColor(product.sustainability_grade) }}>
            <span style={{ color: getScoreColor(product.sustainability_grade) }}>
                EcoScore: <strong>{product.sustainability_grade}</strong>
            </span>
            <small>{product.co2_footprint}kg CO2</small>
        </div>
        <div className="qty">x{quantity}</div>
      </div>
    </div>
  );
};

export default ProductCard;