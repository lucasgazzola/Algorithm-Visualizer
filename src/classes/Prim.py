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


# class Grafo:
#     def __init__(self, vertices=None, aristas=None, conexiones=[]):
#         self._conexiones = conexiones
#         self._vertices = vertices if vertices is not None else set()
#         self._aristas = aristas if aristas is not None else set()
#         self._pesos = {}

#         if conexiones:
#             for conexion in conexiones:
#                 self.agregar_arista(conexion)

#     def agregar_arista(self, conexion):
#         if len(conexion) != 3:
#             raise ValueError(
#                 "Una arista debe ser un 3-subconjunto de vértices y peso.")
#         v, w, peso = conexion
#         self._vertices.update([v, w])
#         self._aristas.add(frozenset([v, w]))
#         self._pesos[frozenset([v, w])] = peso


#     def obtener_pesos(self):
#         return self._pesos

#     def adyacentes(self, v):
#         if v not in self._vertices:
#             raise ValueError(f"El vértice {v} no está en el grafo.")
#         adyacentes = set()
#         for arista in self._aristas:
#             if v in arista:
#                 adyacentes.update(arista)
#         adyacentes.discard(v)  # Remove the vertex itself
#         return adyacentes


# # # Ejemplo de uso
# # if __name__ == "__main__":
# #     conexiones = [
# #         ["A", "B", 1],
# #         ["B", "C", 4],
# #         ["C", "D", 20],
# #         ["D", "E", 12],
# #         ["C", "E", 15],
# #         ["E", "F", 7]
# #     ]
# #
# #     try:
# #         G = Grafo(conexiones=conexiones)
# #         print(G.obtener_aristas())
# #         print(G.obtener_pesos())
# #     except ValueError as e:
#         # print(f"Error al crear el grafo: {e}")
