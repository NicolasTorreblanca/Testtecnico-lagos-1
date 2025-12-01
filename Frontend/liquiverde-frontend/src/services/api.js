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
  // Buscar producto por código o nombre
  scan: (query) => api.post('/scan/', { search_query: query }),
  
  // Optimizar lista (Algoritmo Mochila)
  optimize: (listId, data) => api.post(`/shopping-lists/${listId}/optimize/`, data),
  
  // Obtener una lista específica
  getList: (id) => api.get(`/shopping-lists/${id}/`),

  addItem: (listId, productId, quantity=1) => api.post(`/shopping-lists/${listId}/add-item/`, { product_id: productId, quantity }),
};


export default api;