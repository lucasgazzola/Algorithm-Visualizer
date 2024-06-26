class Prim:
    def __init__(self, vertices=None, aristas=None, conexiones=[]):
        self._conexiones = conexiones
        self._vertices = vertices if vertices is not None else set()
        self._aristas = aristas if aristas is not None else set()
        self._pesos = {}

        for arista in self._conexiones:
            v, w, peso = arista
            self._vertices.update([v, w])
            e = frozenset([v, w])
            self._aristas.add(e)
            self._pesos[e] = peso

    def aristas(self):
        return self._aristas

    def pesos(self):
        return self._pesos

    def vertices(self):
        return self._vertices

    def adyacentes(self, v):
        if v not in self._vertices:
            raise ValueError(f"El vértice {v} no está en el grafo.")
        adyacentes = set()
        for arista in self._aristas:
            if v in arista:
                adyacentes.update(arista)
        adyacentes.discard(v)  # Remove the vertex itself
        return adyacentes

    def agregar_arista(self, e):
        if len(e) != 2:
            raise ValueError(
                "Una arista debe ser un 2-subconjunto de vértices.")
        v, w = e
        if v not in self._vertices or w not in self._vertices:
            raise ValueError("Ambos vértices deben estar en el grafo.")
        self._aristas.add(frozenset(e))

    def agregar_vertice(self, v):
        self._vertices.add(v)

    def eliminar_arista(self, e):
        self._aristas.discard(frozenset(e))

    def eliminar_vertice(self, v):
        if v not in self._vertices:
            return
        self._vertices.remove(v)
        self._aristas = {arista for arista in self._aristas if v not in arista}
