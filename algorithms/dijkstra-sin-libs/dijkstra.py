# Implementación del Algoritmo de Dijkstra
def dijkstra(graph, start):
    unvisited_nodes = list(graph.keys())
    distances = {node: float('infinity') for node in unvisited_nodes}
    distances[start] = 0
    previous_nodes = {node: None for node in unvisited_nodes}

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)

        if distances[current_node] == float('infinity'):
            break

        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node

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


# Definición del grafo como un diccionario
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'C': 2, 'D': 5},
    'C': {'D': 1},
    'D': {}
}

# Nodo de inicio y de fin
start_node = 'A'
end_node = 'D'

# Ejecutar el algoritmo de Dijkstra
distances, previous_nodes = dijkstra(graph, start_node)
shortest_path_nodes = shortest_path(previous_nodes, start_node, end_node)

# Imprimir resultados
print("Distancias desde el nodo inicial:", distances)
print("Camino más corto desde", start_node,
      "hasta", end_node, ":", shortest_path_nodes)

# Visualización simplificada del grafo
print("\nGrafo:")
for node in graph:
    for neighbor in graph[node]:
        print(f"{node} --({graph[node][neighbor]})--> {neighbor}")

# Visualización del camino más corto
print("\nCamino más corto:")
for i in range(len(shortest_path_nodes) - 1):
    print(f"{shortest_path_nodes[i]} --> {shortest_path_nodes[i+1]}")
