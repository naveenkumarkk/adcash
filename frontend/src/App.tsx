import "./App.css";
import { OffersPage } from "./components/OfferPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { HomeIcon } from "@heroicons/react/24/solid";
import { useState } from "react";

export default function App() {
  const [resetKey, setResetKey] = useState(0);

  const handleReset = () => {
    setResetKey((prev) => prev + 1);
  };

  return (
    <Router>
      <header className="header">
        <HomeIcon className="home-icon" onClick={handleReset} />
        <span className="title">ADCash Offer</span>
      </header>

      <Routes>
        <Route path="/" element={<OffersPage key={resetKey} />} />
        <Route path="/offers/all" element={<OffersPage key={resetKey} />} />
      </Routes>
    </Router>
  );
}

