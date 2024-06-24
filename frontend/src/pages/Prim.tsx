import { useState } from 'react'
import FormAgregarConexion from '../components/FormAgregarConexion'

type Conexion = [string, string, number]

export default function Prim() {
  // [['A', 'B', 1], ['A', 'C', 4], ['B', 'C', 2], ['B', 'D', 5], ['C', 'D', 1]]
  const [conexiones, setConexiones] = useState<Conexion[]>([])
  const [agregando, setAgregando] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [pngUrl, setPngUrl] = useState('')

  const handleAgregarConexion = () => {
    setAgregando(true)
  }

  const handleDownload = () => {
    if (!pngUrl) return

    // Create a link element and trigger the download
    const a = document.createElement('a')
    a.href = pngUrl
    a.download = 'mst.png' // Set the default filename here
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
  }

  const handleCalcular = async () => {
    setIsModalOpen(true)
    const response = await fetch('http://localhost:4000/prim', {
      method: 'POST',
      headers: {
        'Content-Type': 'image/png',
      },
      body: JSON.stringify({ conexiones }),
    })

    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
    const image = await response.blob()
    if (image) {
      const imageUrl = URL.createObjectURL(image)
      setPngUrl(imageUrl)
    }
  }

  return (
    <div className="flex flex-col items-center flex-1">
      <h1 className="text-3xl">Prim</h1>
      <ul className="pt-5 flex flex-col gap-2 mb-4">
        {conexiones.length > 0 &&
          conexiones.map(conexion => (
            <li key={`${conexion[0]}-${conexion[1]}-${conexion[2]}`}>
              <span className="text-lg">
                {conexion[0]} - {conexion[1]} {'->'} Peso: {conexion[2]}
                <button
                  onClick={() =>
                    setConexiones(prevConexiones =>
                      prevConexiones.filter(
                        (c: Conexion) =>
                          !(c[0] === conexion[0] && c[1] === conexion[1])
                      )
                    )
                  }
                  type="button"
                  className="bg-red-500 px-1 ml-3">
                  x
                </button>
              </span>
            </li>
          ))}
      </ul>
      {agregando && (
        <FormAgregarConexion
          className="flex flex-col p-2 gap-2 items-end"
          setAgregando={setAgregando}
          setConexiones={setConexiones}
        />
      )}
      {!agregando && (
        <button
          onClick={handleAgregarConexion}
          className="p-2 text-xl font-bold bg-blue-400"
          type="button">
          <span>Nueva</span>
        </button>
      )}
      {isModalOpen && (
        <div className="bg-zinc-800 opacity-95 z-10 absolute top-0 left-0 flex flex-col items-center justify-center w-full h-full">
          <div className="relative flex flex-col gap-5 justify-center items-center h-full w-full">
            <div className="relative">
              <img src={pngUrl} className="w-full" />
              <button
                onClick={() => setIsModalOpen(false)}
                type="button"
                className="absolute top-0 right-0 bg-red-500 border-red-500 p-2 inline-flex items-center justify-center text-zinc-50 hover:bg-red-700 active:bg-red-900">
                <span className="sr-only">Close menu</span>
                <svg
                  className="h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            <button
              onClick={handleDownload}
              className="bg-cyan-500 hover:bg-zinc-800 hover:text-cyan-500 border-cyan-500 border-2 text-zinc-950 font-bold py-2 px-4 rounded inline-flex items-center">
              <svg
                className="fill-current w-4 h-4 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20">
                <path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" />
              </svg>
              <span>Download</span>
            </button>
          </div>
        </div>
      )}
      <div className="mt-auto flex flex-col gap-2">
        <button
          onClick={() => setConexiones([])}
          className="p-2 text-xl font-bold hover:bg-red-400 active:bg-red-800 bg-red-600"
          type="button">
          <span>Borrar Conexiones</span>
        </button>
        <button
          onClick={handleCalcular}
          className="p-2 text-xl font-bold hover:bg-green-400 active:bg-green-800 bg-green-600"
          type="button">
          <span>Calcular</span>
        </button>
      </div>
    </div>
  )
}
