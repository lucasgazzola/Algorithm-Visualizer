import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Home, NotFound } from './pages';
import { AlgorithmLayout } from './layouts';
import { ALGORITHM_LIST } from './constants';
import './App.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                {ALGORITHM_LIST.map((algorithm) => (
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
    );
}

export default App;
