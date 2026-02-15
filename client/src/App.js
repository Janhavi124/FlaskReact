import { useEffect, useState } from "react";
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
  const [authenticated, setAuthenticated] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    fetch("https://flaskreact-production-d646.up.railway.app/check_auth", {
      credentials: "include"
    })
    .then(res => res.json())
    .then(data => {
      setAuthenticated(data.authenticated);
      
      if (!data.authenticated && !['/login', '/register'].includes(location.pathname)) {
        console.log("Not authenticated, redirecting to login"); // ADD THIS
        navigate('/login');
      }
    });
  }, [navigate, location]);

  if (authenticated === null) {
    return <div>Loading...</div>;
  }

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