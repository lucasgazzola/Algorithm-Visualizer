import { Dijkstra, FlujoMaximo, Prim } from '../pages'
import { type Algorithm } from '../types/Algorithm'

const BASE_URL = 'http://localhost:4000'

export const ALGORITHM_LIST: Algorithm[] = [
  {
    id: 1,
    nombre: 'Dijkstra',
    url: BASE_URL + '/dijkstra',
    relativeUrl: '/dijkstra',
    element: <Dijkstra />,
  },
  {
    id: 2,
    nombre: 'Flujo Maximo',
    url: BASE_URL + '/flujo-maximo',
    relativeUrl: '/flujo-maximo',
    element: <FlujoMaximo />,
  },
  {
    id: 3,
    nombre: 'Prim',
    url: BASE_URL + '/prim',
    relativeUrl: '/prim',
    element: <Prim />,
  },
]
