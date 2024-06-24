import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Home, NotFound } from './pages'
import { AlgorithmLayout } from './layouts'
import './App.css'

import { ALGORITHM_LIST } from './constants'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        {ALGORITHM_LIST.map(algorithm => (
          <Route
            key={algorithm.id}
            path={algorithm.relativeUrl}
            element={
              <AlgorithmLayout name={algorithm.nombre}>
                {algorithm.element}
              </AlgorithmLayout>
            }
          />
        ))}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
