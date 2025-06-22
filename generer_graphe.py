import random


def generer_graphe(n, p, oriente=False, pondere=False, poids_min=1, poids_max=10, alphabetique=False):
    """
    Génère un graphe aléatoire avec sommets soit entiers, soit lettres.
    
    Args:
        n (int): Nombre de sommets
        p (float): Probabilité d’existence d’une arête (entre 0 et 1)
        oriente (bool): Si True, graphe orienté
        pondere (bool): Si True, arêtes pondérées
        poids_min (int): Poids minimal si pondéré
        poids_max (int): Poids maximal si pondéré
        alphabetique (bool): Si True, sommets nommés 'A', 'B', ..., 'Z'
        
    Retourne:
        dict: Graphe sous forme {sommet: [(poids, voisin), ...]}
    """
    if not 0 <= p <= 1:
        raise ValueError("La probabilité p doit être entre 0 et 1")
    if pondere and poids_min > poids_max:
        raise ValueError("poids_min doit être <= poids_max")
    if alphabetique and n > 26:
        raise ValueError("Maximum 26 sommets si noms alphabétiques simples")

    # Génération des sommets
    if alphabetique:
        sommets = [chr(65 + i) for i in range(n)]  # 'A', 'B', ..., 'Z'
    else:
        sommets = list(range(n))  # 0, 1, ..., n-1

    graphe = {s: [] for s in sommets}

    for i in range(n):
        start_j = i + 1 if not oriente else 0
        for j in range(start_j, n):
            if i == j:
                continue
            if random.random() < p:
                u, v = sommets[i], sommets[j]
                poids = random.randint(poids_min, poids_max) if pondere else 1
                graphe[u].append((poids, v))
                if not oriente:
                    graphe[v].append((poids, u))
                    
    return graphe




def afficher_graphe(g):
    for u in g:
        print(f"{u} -> {g[u]}")

def main():
    n = 20           # Nombre de sommets
    p = 0.4          # Probabilité d'une arête
    oriente = False
    pondere = True
    alphabetique = False
    g = generer_graphe(n, p, oriente=oriente, pondere=pondere, alphabetique=alphabetique)
    afficher_graphe(g)

    

#main()
