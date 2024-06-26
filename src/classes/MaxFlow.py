import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque


class MaxFlow:
    def __init__(self, connections):
        self.start = ""
        self.end = ""
        self.nodes = set()
        self.edges = set()
        self.connections = connections
        self.indice_a_nodo = {}
        self.nodo_a_indice = {}
        self.graph = self.construir_graph(self.connections)
        self.ROW = len(self.graph)

    '''Returns true if there is a path from source 's' to sink 't' in
    residual graph. Also fills parent[] to store the path '''

    def get_nodes(self):
        return self.nodes

    def BFS(self, s, t, parent):

        # Mark all the vertices as not visited
        visited = [False]*(self.ROW)

        # Create a queue for BFS
        queue = []

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BFS Loop
        while queue:

            # Dequeue a vertex from queue and print it
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and int(val) > 0:
                    # If we find a connection to the sink node,
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
                    if ind == t:
                        return True

        # We didn't reach sink in BFS starting
        # from source, so return false
        return False

    # Returns the maximum flow from s to t in the given graph

    def FordFulkerson(self, source, sink):
        self.start = source
        self.end = sink
        source = self.nodo_a_indice[source]
        sink = self.nodo_a_indice[sink]
        # This array is filled by BFS and to store path
        parent = [-1]*(self.ROW)

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink

        while self.BFS(source, sink, parent):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, int(self.graph[parent[s]][s]))
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while (v != source):
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            return max_flow

    def construir_graph(self, connections):
        # Extraer nodos únicos

        for connection in connections:
            self.edges.add((connection[0], connection[1]))
            self.nodes.add(connection[0])
            self.nodes.add(connection[1])

        # Mapear nodos a índices
        self.nodo_a_indice = {nodo: i for i, nodo in enumerate(self.nodes)}
        self.indice_a_nodo = {i: nodo for nodo,
                              i in self.nodo_a_indice.items()}

        # Inicializar la matriz de adyacencia
        n = len(self.nodes)
        matriz_adyacencia = [[0] * n for _ in range(n)]

        # Llenar la matriz de adyacencia
        for connection in connections:
            desde, hasta, capacidad = connection
            i = self.nodo_a_indice[desde]
            j = self.nodo_a_indice[hasta]
            matriz_adyacencia[i][j] = int(capacidad)
        return matriz_adyacencia

    def graficar_grafo_residual(self, max_flow, filename):
        G = nx.Graph()  # Cambiamos a Graph() para líneas sin dirección
        for i, row in enumerate(self.graph):
            for j, val in enumerate(row):
                if val > 0:
                    desde = self.indice_a_nodo[i]
                    hasta = self.indice_a_nodo[j]
                    G.add_node(desde)
                    G.add_node(hasta)
                    G.add_edge(desde, hasta, capacity=val)
                    if self.graph[j][i] > 0:
                        G.add_edge(hasta, desde, capacity=self.graph[j][i])

        # for u, v, d in G.edges(data=True):
        #     print("u ", u, " v ", v, " d ", d)
        #     print()
        #     print()
        pos = nx.spring_layout(G)
        edge_labels = {(u, v): f"""{u}/{v}: {self.graph[self.nodo_a_indice[u]][self.nodo_a_indice[v]]}/{
            self.graph[self.nodo_a_indice[v]][self.nodo_a_indice[u]]}""" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_nodes(G, pos, node_size=700,
                               node_color="lightblue")
        nx.draw_networkx_labels(G, pos)

        nx.draw_networkx_edges(
            G, pos, edgelist=G.edges(), width=2)
        textstr = f"""Flujo máximo desde {self.start} hasta {self.end}: {
            max_flow}"""
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.gcf().text(0.02, 0.02, textstr, fontsize=12, ha='left')
        plt.savefig(filename)
        plt.clf()
