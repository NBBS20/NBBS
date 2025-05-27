import math

def make_graph():
    # tuple = (poids, noeud_suiv)
        return {
        'A': [(4, 'B'), (2, 'C')],
        'B': [(3, 'C'), (3, 'E'), (2, 'D')],
        'C': [(1, 'B'), (4, 'D'), (5, 'E')],
        'D': [],
        'E': [(1, 'D')],
    }

def initialisation(graphe, s_deb):
    d = {s: math.inf for s in graphe}  # Dictionnaire des distances (infini par défaut)
    d[s_deb] = 0  # La distance du sommet de départ à lui-même est 0
    predecesseur = {s: None for s in graphe}  # Dictionnaire des prédécesseurs
    return d, predecesseur

def trouve_min(Q, d):
    mini = math.inf
    sommet = None
    for s in Q:  # Parcourt tous les sommets non visités
        if d[s] < mini:  # Si on trouve une distance plus petite
            mini = d[s]
            sommet = s
    return sommet

def maj_distances(d, predecesseur, s1, s2, poids):
    if d[s2] > d[s1] + poids:  # Si un chemin plus court est trouvé
        d[s2] = d[s1] + poids  # Met à jour la distance
        predecesseur[s2] = s1  # Met à jour le prédécesseur

def dijkstra(graphe, s_deb):
    d, predecesseur = initialisation(graphe, s_deb)
    Q = set(graphe.keys())  # Ensemble des sommets à visiter
    
    while Q:  # Tant qu'il reste des sommets à visiter
        s1 = trouve_min(Q, d)  # Prend le sommet non visité le plus proche
        Q.remove(s1)  # Le marque comme visité
        
        for poids, s2 in graphe[s1]:  # Pour chaque voisin de s1
            if s2 in Q:  # Si le voisin n'a pas encore été visité
                maj_distances(d, predecesseur, s1, s2, poids)
    
    return d, predecesseur

def chemin(predecesseur, s_deb, s_fin):
    chemin = []
    s = s_fin
    while s is not None and s != s_deb:  # Remonte les prédécesseurs
        chemin.insert(0, s)  # Ajoute au début de la liste
        s = predecesseur[s]
    
    if s == s_deb:  # Si on a bien remonté jusqu'au départ
        chemin.insert(0, s_deb)
        return chemin
    else:  # Si aucun chemin n'existe
        return None



def main():
    G = make_graph()
    start = 'A'

    d, p = dijkstra(G, start)
    print("Distances :", d)
    print("Chemin de A à D :", chemin(p, 'A', 'D'))


main()
