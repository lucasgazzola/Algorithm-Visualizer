import heapq
import networkx as nx
import matplotlib.pyplot as plt

# Implementación del Algoritmo de Dijkstra


def dijkstra(graph, start):
    pq = [(0, start)]
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    previous_nodes = {vertex: None for vertex in graph}

    while pq:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_vertex
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous_nodes


def shortest_path(previous_nodes, start, target):
    path = []
    current = target
    while current != start:
        path.append(current)
        current = previous_nodes[current]
    path.append(start)
    path.reverse()
    return path


# Crear el grafo con networkx
G = nx.DiGraph()

# Agregar nodos y aristas con pesos
edges = [
    ('A', 'B', 1),
    ('A', 'C', 4),
    ('B', 'C', 2),
    ('B', 'D', 5),
    ('C', 'D', 1)
]

for u, v, weight in edges:
    G.add_edge(u, v, weight=weight)

# Crear el grafo como un diccionario para el algoritmo de Dijkstra
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}

start_node = 'A'
end_node = 'D'
distances, previous_nodes = dijkstra(graph, start_node)
shortest_path_nodes = shortest_path(previous_nodes, start_node, end_node)

print("Distancias: ", distances)
print("Camino más corto: ", shortest_path_nodes)

# Especificar manualmente las posiciones de los nodos
pos = {
    'A': (0, 0),
    'B': (1, 1),
    'C': (2, 0),
    'D': (3, 1)
}

# Dibujar el grafo inicial
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=500, font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Grafo Inicial")
plt.savefig('grafo_inicial.png')

# Dibujar el grafo y resaltar el camino más corto
path_edges = [(shortest_path_nodes[i], shortest_path_nodes[i + 1])
              for i in range(len(shortest_path_nodes) - 1)]
plt.figure(figsize=(10, 6))
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=500, font_size=10, font_weight='bold')
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title("Camino más corto resaltado")
plt.savefig('camino_mas_corto.png')
