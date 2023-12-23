import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './components/Home';
import YOLO from './components/YOLO';
import Contact from './components/Contact';
import LoginSignup from './components/LoginSignup';
import Dashboard from './components/Dashboard';
import Objectdetection from './components/Objectdetection'
import Vehicledetection from './components/VehicleCrash'
import Falldetection from './components/FallDetection'
import Socialdetection from './components/SocialDistancing'
function App() {
  
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/yolo" element={<YOLO />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login-signup" element={<LoginSignup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/object-detection" element={<Objectdetection />} />
        <Route path="/vehicle-detection" element={<Vehicledetection />} />
        <Route path="/fall-detection" element={<Falldetection />} />
        <Route path="/social-distancing" element={<Socialdetection />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
