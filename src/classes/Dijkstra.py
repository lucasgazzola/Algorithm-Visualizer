class Dijkstra:
    def __init__(self, conexiones=None):
        self._conexiones = conexiones if conexiones is not None else []
        self._vertices = set()
        self._aristas = set()
        self._pesos = {}

        for conexion in self._conexiones:
            if len(conexion) != 3:
                raise ValueError(
                    "Cada conexión debe contener un par de vértices y un peso.")
            v, w, peso = conexion
            self._vertices.update([v, w])
            # Asegurarse de que la arista sea una tupla de dos elementos
            e = (v, w)
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
                adyacentes.add(arista)
        adyacentes.discard(v)  # Remove the vertex itself
        return adyacentes

    def agregar_arista(self, e):
        if len(e) != 3:
            raise ValueError(
                "Una arista debe ser un 3-subconjunto de vértices y peso.")
        v, w, peso = e
        if v not in self._vertices or w not in self._vertices:
            raise ValueError("Ambos vértices deben estar en el grafo.")
        self._aristas.add((v, w))
        self._pesos[(v, w)] = peso

    def agregar_vertice(self, v):
        self._vertices.add(v)

    def eliminar_arista(self, e):
        self._aristas.discard(e)
        self._pesos.pop(e, None)

    def eliminar_vertice(self, v):
        if v not in self._vertices:
            return
        self._vertices.remove(v)
        self._aristas = {arista for arista in self._aristas if v not in arista}
        self._pesos = {arista: peso for arista,
                       peso in self._pesos.items() if v not in arista}
