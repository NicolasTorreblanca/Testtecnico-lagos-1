import React from 'react';

// Ahora recibimos "onRemove" como propiedad opcional
const ProductCard = ({ item, onRemove }) => {
  const { product, is_suggested_alternative, quantity, substitution_details } = item;
  
  const getScoreColor = (grade) => {
    const map = { 'A': '#27ae60', 'B': '#2ecc71', 'C': '#f1c40f', 'D': '#e67e22', 'E': '#e74c3c' };
    return map[grade] || '#95a5a6';
  };

  return (
    <div className={`product-card ${is_suggested_alternative ? 'substituted' : ''}`}>
      
      {/* 1. Imagen */}
      <div className="product-image">
         <div className="img-placeholder">
            {product.image_url ? 
              <img src={product.image_url} alt={product.name} style={{width:'100%', borderRadius:'50%'}}/> 
              : product.name.charAt(0)}
         </div>
      </div>
      
      {/* 2. Detalles */}
      <div className="product-details">
        <div className="header-row">
            <h3>{product.name}</h3>
            {is_suggested_alternative && <span className="badge-sub">✨ Eco-Smart</span>}
        </div>
        <p className="category">{product.brand} • {product.category}</p>
        
        {is_suggested_alternative && substitution_details && (
             <div className="sub-reason">💡 {substitution_details.reason}</div>
        )}
      </div>

      {/* 3. Métricas y Acciones */}
      <div className="product-metrics">
        <div className="price-tag">${parseInt(product.price).toLocaleString()}</div>
        <div className="eco-badge" style={{ borderColor: getScoreColor(product.sustainability_grade) }}>
            <span style={{ color: getScoreColor(product.sustainability_grade) }}>
                Eco: <strong>{product.sustainability_grade}</strong>
            </span>
        </div>
        
        <div className="actions-row" style={{marginTop: '10px', display:'flex', alignItems:'center', justifyContent:'flex-end', gap:'10px'}}>
            <span className="qty">x{quantity}</span>
            
            {/* BOTÓN ELIMINAR (Solo aparece si pasamos la función onRemove) */}
            {onRemove && (
                <button 
                    onClick={() => onRemove(item.id)} 
                    style={{
                        background:'#ffeded', border:'1px solid #ffcccc', 
                        color:'#e74c3c', borderRadius:'4px', cursor:'pointer', padding:'2px 8px'
                    }}
                    title="Eliminar de la lista"
                >
                    🗑️
                </button>
            )}
        </div>
      </div>
    </div>
  );
};

export default ProductCard;