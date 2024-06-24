import heapq
import networkx as nx
import matplotlib.pyplot as plt
import random

from src.classes import Prim, Dijkstra


def dijkstra(G, start):
    distances = {v: float('infinity') for v in G.vertices()}
    distances[start] = 0
    parents = {v: None for v in G.vertices()}
    visited = set()

    while len(visited) < len(G.vertices()):
        current = min((v for v in G.vertices() if v not in visited),
                      key=lambda x: distances[x])
        visited.add(current)

        for neighbor in G.adyacentes(current):
            if neighbor not in visited:
                weight = next(w for (v_ini, v_fin, w) in G.aristas()
                              if v_ini == current and v_fin == neighbor)
                if distances[current] + weight < distances[neighbor]:
                    distances[neighbor] = distances[current] + weight
                    parents[neighbor] = current

    return distances, parents


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


def draw_dijkstra(G, path, filename="graph.png", layout="spring"):
    """
    Dibuja el grafo G y resalta en verde las aristas del camino más corto proporcionado.

    :param G: Instancia de la clase Grafo.
    :param path: Lista de nodos que representan el camino más corto.
    :param filename: Nombre del archivo donde se guardará la imagen del grafo.
    :param layout: Layout para distribuir los nodos (default: spring).
    """
    graph_nx = nx.DiGraph()  # Crear un grafo dirigido

    # Añadir vértices y aristas al grafo de networkx
    for v in G.vertices():
        graph_nx.add_node(v)
    for e in G.aristas():
        # Asegúrate de que e es una tupla o lista con exactamente dos elementos
        if len(e) != 2:
            raise ValueError(
                "Una arista debe ser un 2-subconjunto de vértices.")

        v, w = e  # Desempaquetar la arista en v y w
        graph_nx.add_edge(v, w, weight=G.pesos()[e])

    # Usar el layout seleccionado
    if layout == "spring":
        pos = nx.spring_layout(graph_nx, seed=42)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(graph_nx)
    elif layout == "shell":
        pos = nx.shell_layout(graph_nx)
    elif layout == "spectral":
        pos = nx.spectral_layout(graph_nx)
    elif layout == "circular":
        pos = nx.circular_layout(graph_nx)
    else:
        raise ValueError("Layout no reconocido")

    # Dibujar todos los nodos y aristas del grafo original
    nx.draw_networkx_nodes(graph_nx, pos, node_size=700,
                           node_color="lightblue")
    nx.draw_networkx_labels(graph_nx, pos, font_size=12, font_color="black")
    nx.draw_networkx_edges(graph_nx, pos, edgelist=graph_nx.edges(
    ), width=2, arrows=True, arrowstyle='-|>', arrowsize=20)

    # Resaltar las aristas del camino más corto en verde, si se proporciona
    if path:
        dijkstra_edges = []
        for i in range(len(path) - 1):
            dijkstra_edges.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(
            graph_nx, pos, edgelist=dijkstra_edges, width=2, edge_color="green", arrowstyle='-|>', arrowsize=20)

    # Mostrar pesos de las aristas
    edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
    nx.draw_networkx_edge_labels(
        graph_nx, pos, edge_labels=edge_labels, font_size=10)

    plt.title("Grafo con camino más corto resaltado en verde")
    plt.savefig(filename)

    # Limpiar el plot para evitar superposiciones en futuras visualizaciones
    plt.clf()


# def dijkstra(graph, start_vertex):
#     # Inicialización de distancias, padres y vistos
#     distances = {vertex: float('infinity') for vertex in graph.vertices()}
#     parents = {vertex: None for vertex in graph.vertices()}
#     seen = {vertex: False for vertex in graph.vertices()}
#     distances[start_vertex] = 0

#     priority_queue = [(0, start_vertex)]
#     heapq.heapify(priority_queue)

#     while priority_queue:
#         current_distance, current_vertex = heapq.heappop(priority_queue)

#         if seen[current_vertex]:
#             continue

#         seen[current_vertex] = True

#         for neighbor in graph.adyacentes(current_vertex):
#             weight = graph.pesos()[frozenset([current_vertex, neighbor])]
#             distance = current_distance + weight

#             if not seen[neighbor] and distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 parents[neighbor] = current_vertex
#                 heapq.heappush(priority_queue, (distance, neighbor))

#     return distances, parents


def obtener_camino(padre, nodo_final):
    """
    Obtiene el camino más corto desde el nodo fuente hasta el nodo final usando el diccionario de padres.
    :param padre: Diccionario de padres.
    :param nodo_final: Nodo final.
    :return: Lista de nodos que forman el camino más corto.
    """
    camino = []
    while nodo_final is not None:
        camino.append(nodo_final)
        nodo_final = padre[nodo_final]
    return camino[::-1]
