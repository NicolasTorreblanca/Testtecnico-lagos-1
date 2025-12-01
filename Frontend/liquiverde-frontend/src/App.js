import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './Components/NavBar';  // Nota el punto único "."
import ShoppingListOptimizer from './Pages/ShoppingListOptimizer';
import ProductScanner from './Pages/ProductScanner';
import ImpactDashboard from './Pages/ImpactDashboard';

// CSS Global
import './App.css';

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Barra de navegación siempre visible */}
        <Navbar />

        {/* El contenido cambia según la URL */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<ShoppingListOptimizer />} />
            <Route path="/scanner" element={<ProductScanner />} />
            <Route path="/dashboard" element={<ImpactDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;