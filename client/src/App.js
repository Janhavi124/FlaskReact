import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import MakeFlavor from './Pages/MakeFlavor'; 
import { UpdateInventory } from './Pages/UpdateInventory';
import { HomePage } from './Pages/HomePage';
import { ViewInventory } from './Pages/ViewInventory';
import { Login } from './Pages/login';
import { Register } from './Pages/register';
import { Layout } from './Layout';
import '@picocss/pico/css/pico.min.css';
import './App.css';

function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      if (!['/login', '/register'].includes(location.pathname)) {
        navigate('/login');
      }
      return;
    }

    fetch("https://flaskreact-production-d646.up.railway.app/check_auth", {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(res => res.json())
    .then(data => {
      if (!data.authenticated && !['/login', '/register'].includes(location.pathname)) {
        localStorage.removeItem('token');
        localStorage.removeItem('user_name');
        navigate('/login');
      }
    })
    .catch(() => {
      if (!['/login', '/register'].includes(location.pathname)) {
        localStorage.removeItem('token');
        localStorage.removeItem('user_name');
        navigate('/login');
      }
    });
  }, [navigate, location]);

  return (
    <Routes>
      <Route element={<Layout/>}>
        <Route path="/" element={<HomePage/>}/> 
        <Route path="/UpdateInventory" element={<UpdateInventory/>}/> 
        <Route path="/MakeFlavor" element={<MakeFlavor/>}/>
        <Route path="/ViewInventory" element={<ViewInventory/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
      </Route>
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;