import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import defaultdict, deque
from src.classes import Prim, Dijkstra


def max_flow(graph, start, end):
    """
    Find the maximum flow in a graph using the Ford-Fulkerson algorithm.

    :param graph: A dictionary representing the graph.
    :param start: The starting node.
    :param end: The ending node.
    :return: The maximum flow in the graph.
    """
    # Initialize the residual graph
    residual_graph = {node: {} for node in graph}
    for node in graph:
        for neighbor, weight in graph[node].items():
            residual_graph[node][neighbor] = weight

    # Find the maximum flow
    max_flow_value = 0
    while augmenting_path(residual_graph, start, end):
        path_flow = float('inf')
        for i in range(len(path) - 1, 0, -1):
            node = path[i]
            neighbor = path[i - 1]
            path_flow = min(path_flow, residual_graph[neighbor][node])
        for i in range(len(path) - 1, 0, -1):
            node = path[i]
            neighbor = path[i - 1]
            residual_graph[node][neighbor] -= path_flow
            residual_graph[neighbor][node] += path_flow
        max_flow_value += path_flow

    return max_flow_value


# Implementar un clase Grafo donde los vértices es un conjunto y las aristas es un conjunto de 2-subconjuntos de vértices.
# Los 2-subconjuntos se implementan con frozenset({v, w}) si v, w vértices (pues Python no admite conjuntos de conjuntos)
# Las funciones y métodos son los obvios. Si G es grafo:
#     G.vertices(): es el conjunto de vértices
#     G.aristas(): es el conjunto de aristas
#     G.adyacentes(v): es el conjunto de vértices adyacentes a un vértice v
#     G.agregar_arista(e): agrega la arista e


# Algoritmo de Prim (revisado)
def prim(G):
    # Inicialización de variables
    r = next(iter(G.vertices()))  # Tomar un vértice de G sin quitarlo
    # Diccionarios para la cola de prioridad y el árbol de expansión mínima (MST)
    clave, padre = {}, {}
    INFINITO = float('inf')  # Valor infinito para inicializar las claves

    # Inicializar todas las claves con INFINITO y los padres con None
    for u in G.vertices():
        clave[u] = INFINITO
        padre[u] = None

    clave[r] = 0  # La clave del primer vértice elegido es 0
    cola = G.vertices().copy()  # Copiar el conjunto de vértices para iterar

    while cola:
        # Seleccionar vértice con la menor clave en la cola
        u = min(cola, key=lambda v: clave[v])
        cola.remove(u)

        # Actualizar las claves y padres de los vértices adyacentes
        for v in G.adyacentes(u):
            e = frozenset({u, v})
            if v in cola and int(G.pesos()[e]) < clave[v]:
                padre[v] = u
                clave[v] = int(G.pesos()[e])

    # Construir y devolver el MST como instancia de Grafo
    mst = Prim(G.vertices(), set())  # MST inicialmente vacío
    for v in mst.vertices() - {r}:
        mst.agregar_arista(frozenset({v, padre[v]}))

    return mst


def draw_prim(G, mst=None, filename="graph.png"):
    """
    Dibuja el grafo G y resalta en rojo las aristas del MST (si se proporciona).

    :param G: Instancia de la clase Grafo.
    :param mst: Instancia de la clase Grafo correspondiente al MST de G. (Opcional)
    """
    graph_nx = nx.Graph()
    filename = "mst.png"
    # Añadir vértices y aristas al grafo de networkx
    for v in G.vertices():
        graph_nx.add_node(v)
    for e in G.aristas():
        v, w = list(e)
        graph_nx.add_edge(v, w, weight=G.pesos()[e])

    pos = nx.spring_layout(graph_nx)

    # Dibujar todos los nodos y aristas del grafo original
    nx.draw_networkx_nodes(graph_nx, pos, node_size=700,
                           node_color="lightblue")
    nx.draw_networkx_labels(graph_nx, pos)
    nx.draw_networkx_edges(graph_nx, pos, edgelist=graph_nx.edges(), width=2)

    # Resaltar las aristas del MST en rojo, si se proporciona
    if mst:
        mst_edges = []
        for e in mst.aristas():
            mst_edges.append(tuple(e))
        nx.draw_networkx_edges(
            graph_nx, pos, edgelist=mst_edges, width=2, edge_color="red")

    # Mostrar pesos de las aristas
    edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
    nx.draw_networkx_edge_labels(graph_nx, pos, edge_labels=edge_labels)

    plt.title("Grafo con MST resaltado en rojo")
    plt.savefig(filename)

    # Mostrar el grafo en una nueva ventana
    # plt.show()

    plt.clf()


def dijkstra(G, start, end):
    dist = {v: float('inf') for v in G.vertices()}
    prev = {v: None for v in G.vertices()}
    dist[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_dist, u = heapq.heappop(priority_queue)

        if u == end:
            break

        for v in G.adyacentes(u):
            e = (u, v)
            weight = G.pesos()[e]
            distance = int(current_dist) + int(weight)

            if distance < dist[v]:
                dist[v] = distance
                prev[v] = u
                heapq.heappush(priority_queue, (distance, v))

    # Reconstruir el camino
    path = deque()
    u = end
    if prev[u] or u == start:
        while u:
            path.appendleft(u)
            u = prev[u]

    return dist, list(path)


# def draw_dijkstra(G, path=None, filename="dijkstra.png"):
#     """
#     Dibuja el grafo G y resalta en rojo las aristas del camino más corto (si se proporciona).

#     :param G: Instancia de la clase Grafo.
#     :param path: Lista de nodos que representa el camino más corto. (Opcional)
#     """
#     graph_nx = nx.DiGraph()
#     filename = "dijkstra.png"

#     # Añadir vértices y aristas al grafo de networkx
#     for v in G.vertices():
#         graph_nx.add_node(v)
#     for e in G.aristas():
#         v, w = e
#         graph_nx.add_edge(v, w, weight=G.pesos()[e])

#     pos = nx.spring_layout(graph_nx)

#     # Dibujar todos los nodos y aristas del grafo original
#     nx.draw_networkx_nodes(graph_nx, pos, node_size=700,
#                            node_color="lightblue")
#     nx.draw_networkx_labels(graph_nx, pos)
#     nx.draw_networkx_edges(graph_nx, pos, edgelist=graph_nx.edges(), width=2)

#     # Resaltar las aristas del camino más corto en rojo, si se proporciona
#     if path:
#         path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
#         nx.draw_networkx_edges(
#             graph_nx, pos, edgelist=path_edges, width=2, edge_color="red")

#     # Mostrar pesos de las aristas
#     edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
#     nx.draw_networkx_edge_labels(graph_nx, pos, edge_labels=edge_labels)

#     plt.title("Grafo con el camino más corto resaltado en rojo")
#     plt.savefig(filename)

#     # Mostrar el grafo en una nueva ventana
#     # plt.show()

#     plt.clf()

def draw_dijkstra(G, path=None, distance=None, start=None, end=None, filename="dijkstra.png"):
    """
    Dibuja el grafo G y resalta en rojo las aristas del camino más corto (si se proporciona).

    :param G: Instancia de la clase Grafo.
    :param path: Lista de nodos que representa el camino más corto. (Opcional)
    :param distance: Distancia total del camino más corto. (Opcional)
    :param start: Nodo de inicio del camino más corto. (Opcional)
    :param end: Nodo final del camino más corto. (Opcional)
    """
    graph_nx = nx.DiGraph()
    filename = "dijkstra.png"

    # Añadir vértices y aristas al grafo de networkx
    for v in G.vertices():
        graph_nx.add_node(v)
    for e in G.aristas():
        v, w = e
        graph_nx.add_edge(v, w, weight=G.pesos()[e])

    pos = nx.spring_layout(graph_nx)

    # Dibujar todos los nodos y aristas del grafo original
    nx.draw_networkx_nodes(graph_nx, pos, node_size=700,
                           node_color="lightblue")
    nx.draw_networkx_labels(graph_nx, pos)
    nx.draw_networkx_edges(graph_nx, pos, edgelist=graph_nx.edges(
    ), width=2, arrowstyle='->', arrowsize=20)

    # Resaltar las aristas del camino más corto en rojo, si se proporciona
    if path:
        path_edges = [(path[i], path[i+1]) for i in range(len(path) - 1)]
        nx.draw_networkx_edges(
            graph_nx, pos, edgelist=path_edges, width=2, edge_color="red", arrowstyle='->', arrowsize=20)

    # Mostrar pesos de las aristas
    edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
    nx.draw_networkx_edge_labels(graph_nx, pos, edge_labels=edge_labels)

    # Añadir información de distancia y camino más corto
    if distance is not None and start is not None and end is not None:
        textstr = f"Distancia desde {start} hasta {end}: {
            distance}\nCamino más corto: {' -> '.join(path)}"
        plt.gcf().text(0.02, 0.02, textstr, fontsize=12, ha='left')

    plt.title("Grafo con el camino más corto resaltado en rojo")
    plt.savefig(filename)

    # Mostrar el grafo en una nueva ventana
    # plt.show()

    plt.clf()
