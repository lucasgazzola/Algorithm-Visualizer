type StartAndEndProps = {
  setNodoInicial: React.Dispatch<React.SetStateAction<string>>
  setNodoFinal: React.Dispatch<React.SetStateAction<string>>
  agregando: boolean
  nodoInicial: string
  nodoFinal: string
}

function StartAndEnd({
  setNodoInicial,
  setNodoFinal,
  agregando,
  nodoInicial,
  nodoFinal,
}: StartAndEndProps) {
  return (
    <>
      <label
        htmlFor="nodo-inicial"
        className={`flex gap-2 justify-end items-center ${
          agregando && 'mt-auto'
        }`}>
        Nodo inicial:
        <input
          className="outline-none w-10 text-zinc-950 px-2 py-1"
          onChange={e => setNodoInicial(e.target.value.toUpperCase())}
          value={nodoInicial}
          type="text"
          name="nodo-inicial"
          id="nodo-inicial"
          autoComplete="off"
        />
      </label>
      <label
        htmlFor="nodo-final"
        className="flex gap-2 justify-end items-center">
        Nodo final:
        <input
          className="outline-none w-10 text-zinc-950 px-2 py-1"
          onChange={e => setNodoFinal(e.target.value.toUpperCase())}
          value={nodoFinal}
          type="text"
          name="nodo-final"
          id="nodo-final"
          autoComplete="off"
        />
      </label>
    </>
  )
}

export default StartAndEnd
