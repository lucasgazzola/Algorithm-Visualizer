class Dijkstra:
    def __init__(self, vertices=None, aristas=None, conexiones=[]):
        self._conexiones = conexiones
        self._vertices = vertices if vertices is not None else set()
        self._aristas = aristas if aristas is not None else set()
        self._pesos = {}

        for arista in self._conexiones:
            v, w, peso = arista
            self._vertices.update([v, w])
            e = (v, w)  # Directed edge
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
            if v == arista[0]:
                adyacentes.add(arista[1])
        return adyacentes

    def agregar_arista(self, e, peso):
        if len(e) != 2:
            raise ValueError(
                "Una arista debe ser un 2-subconjunto de vértices.")
        v, w = e
        if v not in self._vertices or w not in self._vertices:
            raise ValueError("Ambos vértices deben estar en el grafo.")
        self._aristas.add((v, w))
        self._pesos[(v, w)] = peso

    def agregar_vertice(self, v):
        self._vertices.add(v)

    def eliminar_arista(self, e):
        self._aristas.discard((e[0], e[1]))

    def eliminar_vertice(self, v):
        if v not in self._vertices:
            return
        self._vertices.remove(v)
        self._aristas = {arista for arista in self._aristas if v not in arista}


class Dijkstra:
    def __init__(self, vertices=None, aristas=None, conexiones=[]):
        self._conexiones = conexiones
        self._vertices = vertices if vertices is not None else set()
        self._aristas = aristas if aristas is not None else set()
        self._pesos = {}

        for arista in self._conexiones:
            v, w, peso = arista
            self._vertices.update([v, w])
            e = (v, w)  # Directed edge
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
            if v == arista[0]:
                adyacentes.add(arista[1])
        return adyacentes

    def agregar_arista(self, e, peso):
        if len(e) != 2:
            raise ValueError(
                "Una arista debe ser un 2-subconjunto de vértices.")
        v, w = e
        if v not in self._vertices or w not in self._vertices:
            raise ValueError("Ambos vértices deben estar en el grafo.")
        self._aristas.add((v, w))
        self._pesos[(v, w)] = peso

    def agregar_vertice(self, v):
        self._vertices.add(v)

    def eliminar_arista(self, e):
        self._aristas.discard((e[0], e[1]))

    def eliminar_vertice(self, v):
        if v not in self._vertices:
            return
        self._vertices.remove(v)
        self._aristas = {arista for arista in self._aristas if v not in arista}
