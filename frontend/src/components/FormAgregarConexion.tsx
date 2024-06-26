import { Dispatch, FormEvent, SetStateAction, useState } from 'react'

type Conexion = [string, string, number]
type FormAgregarConexionProps = {
  esDikjstra?: boolean
  setConexiones: Dispatch<SetStateAction<Conexion[]>>
  setAgregando: Dispatch<SetStateAction<boolean>>
  setNodos?: Dispatch<SetStateAction<Set<string>>>
  className?: string
}

export default function FormAgregarConexion({
  esDikjstra = false,
  setConexiones,
  setNodos,
  setAgregando,
  className,
}: FormAgregarConexionProps) {
  const [conexionData, setConexionData] = useState<{
    nodo1: string
    nodo2: string
    peso: number
  }>({ nodo1: '', nodo2: '', peso: 0 })

  const handleAgregarConexion = (e: FormEvent) => {
    e.preventDefault()

    let upperNodo1 = conexionData.nodo1.toUpperCase()
    let upperNodo2 = conexionData.nodo2.toUpperCase()

    if (upperNodo1 === '' || upperNodo2 === '' || !Number(conexionData.peso))
      return

    // Antes de almacenar los nodos en el arreglo de conexiones, los ordenmos por orden alfabético en mayúsculas
    if (upperNodo1 > upperNodo2 && !esDikjstra)
      [upperNodo1, upperNodo2] = [upperNodo2, upperNodo1]

    if (setNodos) {
      setNodos(nodos => new Set([...nodos, upperNodo1, upperNodo2]))
    }

    setConexiones(conexiones => {
      // Chequeamos si ya existe una conexión entre los dos nodos
      const existeConexion = (conexion: Conexion) => {
        return upperNodo1 === conexion[0] && upperNodo2 === conexion[1]
      }

      const nodesConnectionExist = conexiones.some((conexion: Conexion) =>
        existeConexion(conexion)
      )

      if (nodesConnectionExist) {
        // pregunto si quiere reemplazar la existente

        if (
          window.confirm(
            `Ya existe una ruta entre ${upperNodo1} y ${upperNodo2}. ¿Deseas reemplazarla?`
          )
        ) {
          return conexiones.map(conexion => {
            if (existeConexion(conexion)) {
              return [conexion[0], conexion[1], conexionData.peso]
            }
            return conexion
          })
        }

        return conexiones
      }

      return conexiones.concat([[upperNodo1, upperNodo2, conexionData.peso]])
    })

    setAgregando(false)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setConexionData({ ...conexionData, [name]: value.toUpperCase() })
  }

  return (
    <form className={className} onSubmit={handleAgregarConexion}>
      <label htmlFor="nodo1">
        Nodo 1:{' '}
        <input
          id="nodo1"
          name="nodo1"
          type="text"
          required
          autoComplete="off"
          autoFocus
          value={conexionData.nodo1}
          onChange={handleInputChange}
          className="outline-none w-10 text-zinc-950 px-2 py-1"
        />
      </label>

      <label htmlFor="nodo2">
        Nodo 2:{' '}
        <input
          id="nodo2"
          name="nodo2"
          type="text"
          required
          autoComplete="off"
          value={conexionData.nodo2}
          onChange={handleInputChange}
          className="outline-none w-10 text-zinc-950 px-2 py-1"
        />
      </label>

      <label htmlFor="peso">
        Peso:{' '}
        <input
          id="peso"
          name="peso"
          type="number"
          min="0"
          step="1"
          autoComplete="off"
          required
          value={conexionData.peso === 0 ? '' : conexionData.peso}
          onChange={handleInputChange}
          className="outline-none w-14 text-zinc-950 px-2 py-1"
        />
      </label>

      <div className="flex gap-4">
        <button
          className="hover:bg-red-800 active:bg-red-900 bg-red-600 h-10 px-2 rounded-sm flex items-center justify-center self-center"
          type="button"
          onClick={() => setAgregando(false)}>
          <span className="text-xl font-bold">Cerrar</span>
        </button>

        <button
          className="hover:bg-green-800 active:bg-green-900 bg-green-600 rounded-sm flex items-center justify-center self-center w-10 h-10"
          type="submit">
          <span className="text-xl font-bold">+</span>
        </button>
      </div>
    </form>
  )
}
