import "./App.css"
import { OffersPage } from "./components/OfferPage"
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom"
import { HomeIcon } from "@heroicons/react/24/solid"
import { useState } from "react"

// App.tsx
const App = () => {
  const [resetKey, setResetKey] = useState(0)

  return (
    <Router>
      <header className="header">
        <HomeIcon
          className="home-icon"
          onClick={() => setResetKey(prev => prev + 1)}
        />
        <span className="title">ADCash Offer</span>
      </header>

      <Routes>
        <Route
          path="/offers/all"
          element={<OffersPage key={resetKey} />}
        />
        <Route
          path="/"
          element={<OffersPage key={resetKey} />}
        />
      </Routes>
    </Router>
  )
}

export default App

