import heapq
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

# Visualización simplificada del grafo y el camino más corto


def draw_graph(graph, path_edges):
    nodes = graph.keys()
    positions = {
        'A': (0, 0),
        'B': (1, 1),
        'C': (2, 0),
        'D': (3, 1)
    }

    plt.figure(figsize=(10, 6))

    # Dibujar nodos
    for node, (x, y) in positions.items():
        plt.scatter(x, y, s=500, c='lightblue', zorder=2)
        plt.text(x, y, node, fontsize=12, ha='center', va='center', zorder=3)

    # Dibujar aristas
    for start, edges in graph.items():
        for end, weight in edges.items():
            start_pos = positions[start]
            end_pos = positions[end]
            plt.plot([start_pos[0], end_pos[0]], [
                     start_pos[1], end_pos[1]], 'k-', zorder=1)
            plt.text((start_pos[0] + end_pos[0]) / 2, (start_pos[1] +
                     end_pos[1]) / 2, str(weight), color='red', fontsize=12)

    # Resaltar el camino más corto
    for start, end in path_edges:
        start_pos = positions[start]
        end_pos = positions[end]
        plt.plot([start_pos[0], end_pos[0]], [start_pos[1],
                 end_pos[1]], 'r-', linewidth=2, zorder=1)

    plt.title("Grafo con el Camino Más Corto Resaltado")
    plt.axis('off')
    plt.show()


path_edges = [(shortest_path_nodes[i], shortest_path_nodes[i + 1])
              for i in range(len(shortest_path_nodes) - 1)]
draw_graph(graph, path_edges)
