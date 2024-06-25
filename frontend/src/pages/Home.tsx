import { useLocation, useNavigate } from 'react-router-dom';
import AlgorithmLink from '../components/AlgorithmButton';
import { ALGORITHM_LIST } from '../constants';
import { useEffect } from 'react';

export default function Home() {
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        if (location.pathname === '/dijkstra') navigate('/dijkstra');
        if (location.pathname === '/prim') navigate('/prim');
    }, [location.pathname]);

    return (
        <div className="flex flex-col justify-center text-center gap-20 w-full h-full">
            <h1 className="text-4xl font-bold">Seleccione un algoritmo</h1>
            <ul className="flex flex-col justify-center text-center gap-5">
                {ALGORITHM_LIST.map((algorithm) => (
                    <li key={algorithm.id}>
                        <AlgorithmLink algorithm={algorithm} />
                    </li>
                ))}
            </ul>
        </div>
    );
}
