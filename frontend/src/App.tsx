import './App.css'
import { OffersPage } from './components/OfferPage'
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"

function App() {
  return (
    <Router>
      <div className="App">
        <header>ADCash Offer</header>
        <main>
            <Routes>
              <Route path="/" element={<OffersPage />} />
            </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
