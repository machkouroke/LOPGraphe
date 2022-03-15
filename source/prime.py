from heapq import heappop, heappush
from networkx import Graph
from time import perf_counter_ns


def tupleur(x, dict_adj):
    return tuple((dict_adj[i]['weight'], x, i) for i in dict_adj)


def prime_naif(G: Graph, x: 'Noeud de départ') -> tuple[Graph, float]:
    """
    Pour un graphe G donné recherche l'arbre couvrant
    de poids minimum d'une manière naif
    :param G:Graphe ou on cherche l'arbre minimum
    :param x:Point de départ pour rechercher l'arbre
    :return:Arbre minimum sous forme de Graphe
    """
    # Compter les performance de l'algorithme
    start = perf_counter_ns()

    # Minimum Spanning Tree
    mst = Graph()
    mst.add_node(x)

    # Liste component tous les côtés adjacents
    # au nœud contenu dans le sous graphe
    connected = list(tupleur(x, G[x]))
    # Tant que la file n'est pas vide
    while connected:
        # On cherche le minimum de notre liste qu'on va retirer après l'avoir ajouté à l'arbre
        # Il faut noter que le point a est deja contenu dans l'arbre
        weight, a, b = connected.pop(connected.index(min(connected)))

        # si le nouveau point b sélectionné n'est pas dans l'arbre on
        # ajoute le bord à l'arbre
        if b not in mst.nodes:
            mst.add_edge(a, b, weight=weight)
            # On ajoute tous les nœuds adjacents du point b ajoutés à la liste
            connected.extend(tupleur(b, G[b]))
    return mst, perf_counter_ns() - start


def prime_optimized(G: Graph, x: 'Noeud de départ') -> tuple[Graph, float]:
    """
    Pour un graphe G donné recherche l'arbre couvrant
    de poids minimum d'une manière plus efficaces
    :param G:Graphe ou on cherche l'arbre minimum
    :param x:Point de départ pour rechercher l'arbre
    :return:Arbre minimum sous forme de Graphe
    """
    # Compter les performance de l'algorithme
    start = perf_counter_ns()

    # Minimum Spanning Tree
    mst = Graph()
    mst.add_node(x)
    # File de priorité comprenant tous les côtés adjacents
    # au nœud contenu dans le sous graphe
    connected = list(tupleur(x, G[x]))

    # Tant que la file n'est pas vide
    while connected:
        # On retire le minimum grâce à notre file de priorité
        # Il faut noter que le point a est deja contenu dans l'arbre
        weight, a, b = heappop(connected)

        # si le nouveau point b sélectionné n'est pas dans l'arbre on
        # ajoute le bord à l'arbre
        if b not in mst.nodes:
            mst.add_edge(a, b, weight=weight)
            # On ajoute tous les nœuds adjacents des points ajoutés à la file
            # a la file
            for i in tupleur(b, G[b]):
                heappush(connected, i)
    return mst, perf_counter_ns() - start
