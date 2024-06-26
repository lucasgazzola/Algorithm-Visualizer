import networkx as nx
import matplotlib.pyplot as plt

from src.classes import Prim


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

# FUNCIONA
# def draw_prim(G, mst=None, filename="graph.png"):
#     """
#     Dibuja el grafo G y resalta en rojo las aristas del MST (si se proporciona).

#     :param G: Instancia de la clase Grafo.
#     :param mst: Instancia de la clase Grafo correspondiente al MST de G. (Opcional)
#     """
#     graph_nx = nx.Graph()
#     filename = "mst.png"
#     # Añadir vértices y aristas al grafo de networkx
#     for v in G.vertices():
#         graph_nx.add_node(v)
#     for e in G.aristas():
#         v, w = list(e)
#         graph_nx.add_edge(v, w, weight=G.pesos()[e])

#     pos = nx.spring_layout(graph_nx)

#     # Dibujar todos los nodos y aristas del grafo original
#     nx.draw_networkx_nodes(graph_nx, pos, node_size=700,
#                            node_color="lightblue")
#     nx.draw_networkx_labels(graph_nx, pos)
#     nx.draw_networkx_edges(graph_nx, pos, edgelist=graph_nx.edges(), width=2)

#     # Resaltar las aristas del MST en rojo, si se proporciona
#     if mst:
#         mst_edges = []
#         for e in mst.aristas():
#             mst_edges.append(tuple(e))
#         nx.draw_networkx_edges(
#             graph_nx, pos, edgelist=mst_edges, width=2, edge_color="red")

#     # Mostrar pesos de las aristas
#     edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
#     nx.draw_networkx_edge_labels(graph_nx, pos, edge_labels=edge_labels)
#     plt.gcf().text(0.02, 0.02, textstr, fontsize=12, ha='left')
#     plt.title("Grafo con MST resaltado en rojo")
#     plt.savefig(filename)

#     # Mostrar el grafo en una nueva ventana
#     # plt.show()

#     plt.clf()


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

    mst_weight = 0  # Inicializar el peso total del MST

    # Resaltar las aristas del MST en rojo, si se proporciona
    if mst:
        mst_edges = []
        for e in mst.aristas():
            mst_edges.append(tuple(e))
            # Sumar los pesos de las aristas del MST
            mst_weight += int(G.pesos()[e])
        nx.draw_networkx_edges(
            graph_nx, pos, edgelist=mst_edges, width=2, edge_color="red")

    # Mostrar pesos de las aristas
    edge_labels = nx.get_edge_attributes(graph_nx, 'weight')
    nx.draw_networkx_edge_labels(graph_nx, pos, edge_labels=edge_labels)

    # Mostrar el tamaño del MST debajo de la imagen
    textstr = f"Tamaño del Árbol de Expansión Mínima: {mst_weight}"
    plt.gcf().text(0.02, 0.02, textstr, fontsize=12, ha='left')

    plt.title("Grafo con MST resaltado en rojo")
    plt.savefig(filename)

    plt.clf()
