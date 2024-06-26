type BotonAgregarConexionProps = {
  setAgregando: React.Dispatch<React.SetStateAction<boolean>>
}

function BotonAgregarConexion({ setAgregando }: BotonAgregarConexionProps) {
  const handleAgregarConexion = () => {
    setAgregando(true)
  }
  return (
    <button
      onClick={handleAgregarConexion}
      className="mt-auto p-2 text-xl font-bold hover:bg-blue-800 active:bg-blue-900 bg-blue-600"
      type="button">
      <span>Nueva</span>
    </button>
  )
}

export default BotonAgregarConexion
