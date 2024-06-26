import heapq
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


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
        textstr = f"""Distancia desde {start} hasta {end}: {
            distance}\nCamino más corto: {' -> '.join(path)}"""
        plt.gcf().text(0.02, 0.02, textstr, fontsize=12, ha='left')

    plt.title("Grafo con el camino más corto resaltado en rojo")
    plt.savefig(filename)

    # Mostrar el grafo en una nueva ventana
    # plt.show()

    plt.clf()
