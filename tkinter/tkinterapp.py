import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt


class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dijkstra App")
        self.root.geometry("400x400")

        # Crear frame para ingresar nodos y distancias
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill="both", expand=True)

        # Etiquetas y entradas para nodos y distancias
        self.node1_label = tk.Label(self.frame, text="Nodo 1:")
        self.node1_label.pack()
        self.node1_entry = tk.Entry(self.frame)
        self.node1_entry.pack()

        self.node2_label = tk.Label(self.frame, text="Nodo 2:")
        self.node2_label.pack()
        self.node2_entry = tk.Entry(self.frame)
        self.node2_entry.pack()

        self.distance_label = tk.Label(self.frame, text="Distancia:")
        self.distance_label.pack()
        self.distance_entry = tk.Entry(self.frame)
        self.distance_entry.pack()

        # Botón para agregar nodo y distancia
        self.add_button = tk.Button(
            self.frame, text="Agregar", command=self.add_edge)
        self.add_button.pack()

        # Botón para calcular Dijkstra
        self.dijkstra_button = tk.Button(
            self.frame, text="Calcular Dijkstra", command=self.calculate_dijkstra)
        self.dijkstra_button.pack()

        # Grafo
        self.G = nx.Graph()
        self.edges = []

        # Nodo inicial y final
        self.start_node_label = tk.Label(self.frame, text="Nodo inicial:")
        self.start_node_label.pack()
        self.start_node_entry = tk.Entry(self.frame)
        self.start_node_entry.pack()

        self.end_node_label = tk.Label(self.frame, text="Nodo final:")
        self.end_node_label.pack()
        self.end_node_entry = tk.Entry(self.frame)
        self.end_node_entry.pack()

    def add_edge(self):
        node1 = self.node1_entry.get()
        node2 = self.node2_entry.get()
        distance = self.distance_entry.get()
        if node1 and node2 and distance:
            self.edges.append((node1, node2, int(distance)))
            self.node1_entry.delete(0, tk.END)
            self.node2_entry.delete(0, tk.END)
            self.distance_entry.delete(0, tk.END)

    def calculate_dijkstra(self):
        # Agregar edges al grafo
        for node1, node2, weight in self.edges:
            self.G.add_edge(node1, node2, weight=weight)

        # Obtener nodo inicial y final
        start_node = self.start_node_entry.get()
        end_node = self.end_node_entry.get()

        # Ejecutar algoritmo de Dijkstra
        try:
            shortest_path = nx.dijkstra_path(self.G, start_node, end_node)
            shortest_path_length = nx.dijkstra_path_length(
                self.G, start_node, end_node)

            # Mostrar grafo
            pos = nx.spring_layout(self.G)
            nx.draw_networkx(self.G, pos, with_labels=True,
                             node_color='lightblue', node_size=5000)

            # Agregar etiquetas de distancia a las aristas
            edge_labels = {(u, v): d['weight']
                           for u, v, d in self.G.edges(data=True)}
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)

            # Resaltar camino más corto
            nx.draw_networkx_edges(self.G, pos, edgelist=[(
                shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)], edge_color='red', width=2)

            plt.show()

            messagebox.showinfo("Resultados", f"Camino más corto: {
                                shortest_path} con distancia {shortest_path_length}")
        except nx.NetworkXNoPath:
            messagebox.showinfo("Error", "No hay camino entre los nodos")


root = tk.Tk()
app = DijkstraApp(root)
root.mainloop()
