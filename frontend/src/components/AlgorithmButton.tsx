import { Link } from 'react-router-dom'
import { Algorithm } from '../types/Algorithm'

export default function AlgorithmLink({ algorithm }: { algorithm: Algorithm }) {
  return (
    <Link
      className="inline-block px-6 py-3 text-blue-400 border-2 border-blue-400 hover:bg-blue-500 hover:text-white rounded-md"
      to={algorithm.url}>
      <span className="text-4xl font-semibold">{algorithm.nombre}</span>
    </Link>
  )
}
