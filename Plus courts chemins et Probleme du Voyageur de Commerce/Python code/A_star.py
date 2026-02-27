import heapq

infini = float("inf")

def make_graph():
    # tuple = (poids, noeud_suiv)
        return {
        'A': [(4, 'B'), (2, 'C')],
        'B': [(3, 'C'), (3, 'E'), (2, 'D')],
        'C': [(1, 'B'), (4, 'D'), (5, 'E')],
        'D': [],
        'E': [(1, 'D')],
    }

# Distance_totale = cout + heuristique
def heuristique_nulle(n, but):
    """Heuristique simple (fonction h(n)) : ici, h=0 = Dijkstra pur.
    """
    return 0  

import math

def heuristique_euclidienne(noeud, but, coordonnees):
    """Distance euclidienne entre le noeud actuel et le but"""
    x1, y1 = coordonnees[noeud]
    x2, y2 = coordonnees[but]
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def heuristique_manhattan(noeud, but, coordonnees):
    """Distance de Manhattan (somme des différences absolues)"""
    x1, y1 = coordonnees[noeud]
    x2, y2 = coordonnees[but]
    return abs(x1 - x2) + abs(y1 - y2)

def heuristique_alphabet(noeud, but):
    """Différence de position dans l'alphabet"""
    return abs(ord(but) - ord(noeud))


def a_star(graphe, depart, but):
    """Implémentation de A* avec tas"""
    # Initialisation
    d_minimales = {noeud: infini for noeud in graphe} 
    predecesseurs = {noeud: None for noeud in graphe}
    visited = set()  # Ensemble des nœuds visités
    tas = []  # Tas pour sélectionner le prochain nœud à explorer

    # Configuration du départ
    d_minimales[depart] = 0
    f_score = {noeud: infini for noeud in graphe}  # f(n) = g(n) + h(n)
    f_score[depart] = heuristique_euclidienne(depart, but)
    heapq.heappush(tas, (f_score[depart], depart))

    while tas:
        _, noeud = heapq.heappop(tas)
        
        # Si déjà visité, on passe
        if noeud in visited:
            continue
        visited.add(noeud)

        # Si on a atteint le but, on sort
        if noeud == but:
            return d_minimales, predecesseurs, chemin(predecesseurs, depart, but), len(visited)

        # Exploration des voisins
        for poids, voisin in graphe[noeud]:
            if voisin in visited:
                continue

            # Calcul du nouveau coût
            tentative_g = d_minimales[noeud] + poids
            
            # Si meilleur chemin trouvé
            if tentative_g < d_minimales[voisin]:
                d_minimales[voisin] = tentative_g
                predecesseurs[voisin] = noeud
                f_score[voisin] = tentative_g + heuristique_euclidienne(voisin, but)
                heapq.heappush(tas, (f_score[voisin], voisin))

    return None , len(visited)


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
    """Fonction main pour tester l'algorithme"""
    graphe = make_graph()
    depart = 'A'

    distances, p = a_star(graphe, depart, but='D' )

    print(f'A* : Chemins les plus courts depuis {depart} (avec tas): {distances}')
    print("Chemin de A à D :", chemin(p, 'A', 'D'))

# Exécute le programme
#main()
