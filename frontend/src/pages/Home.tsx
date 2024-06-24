import AlgorithmLink from '../components/AlgorithmButton'
import { ALGORITHM_LIST } from '../constants'

export default function Home() {
  return (
    <div className="flex flex-col justify-center text-center gap-20 w-full h-full">
      <h1 className="text-4xl font-bold">Seleccione un algoritmo</h1>
      <ul className="flex flex-col justify-center text-center gap-5">
        {ALGORITHM_LIST.map(algorithm => (
          <li key={algorithm.id}>
            <AlgorithmLink algorithm={algorithm} />
          </li>
        ))}
      </ul>
    </div>
  )
}
