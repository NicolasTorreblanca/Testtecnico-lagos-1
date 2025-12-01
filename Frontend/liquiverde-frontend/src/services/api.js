import axios from 'axios';

// Configuración base de Axios
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Tu backend Django
  headers: {
    'Content-Type': 'application/json',
  },
});

// Endpoints organizados
export const productService = {
  scan: (query) => api.post('/scan/', { search_query: query }),
  optimize: (listId, data) => api.post(`/shopping-lists/${listId}/optimize/`, data),
  getList: (id) => api.get(`/shopping-lists/${id}/`),
  
  // Agregar (Desde el Scanner)
  addItem: (listId, productId, qty=1) => api.post(`/shopping-lists/${listId}/add-item/`, { 
      product_id: productId, 
      quantity: qty 
  }),

  // Eliminar (Desde la Lista) - NUEVO
  removeItem: (listId, itemId) => api.post(`/shopping-lists/${listId}/remove-item/`, { 
      item_id: itemId 
  }),
};


export default api;