def make_graph():
    # tuple = (poids, noeud_suiv)
    return {
        'S': [(8, 'E'), (10, 'A')],
        'A': [(2, 'C')],
        'B': [(1, 'A')],
        'C': [(-2, 'B')],
        'D': [(-4, 'A'), (-1, 'C')],
        'E': [(1, 'D')],
    }

def make_graph_with_negative_cycle():
    return {
        'S': [(8, 'E'), (10, 'A')],
        'A': [(-2, 'C')],
        'B': [(1, 'A')],
        'C': [(-2, 'B')],
        'D': [(-4, 'A'), (-1, 'C')],
        'E': [(1, 'D')],
    }


def bellman_ford (G, source):
        """
        Implémentation de l'algorithme de Bellman-Ford pour trouver les plus courts chemins
        depuis un sommet source dans un graphe pondéré (avec possibilité de poids négatifs)
        
        Args : 
            source : le sommet a partir duquel on fait le parcourt
        
        Returns:
            (distances, predecessors): Un tuple contenant:
                - distances: Dictionnaire des distances minimales depuis source.
                - predecessors: Dictionnaire des prédécesseurs pour reconstruire les chemins.
    
        Raises:
            ValueError: Si le graphe contient un cycle de poids négatif atteignable
        """
        
        # on initialise la liste (dict) des distances a +inf
        distances = {sommet: float('inf') for sommet in G}
        
        # On initialise la liste (dict) des predecesseur a NONE
        predecesseurs = {sommet: None for sommet in G}
    
        distances [source] = 0  # La distance du sommet de lui meme est initialiser a 0
        size = len(G)
        i = 1
        # On parcourt les sommets au plus |V|-1
        for _ in range(size-1):
            updated = False # Flag pour détecter une mise à jour 
            for sommet in G :
                for (cout, succ) in G[sommet] :
                    if distances[sommet] + cout < distances[succ] : 
                        distances[succ] = distances[sommet] + cout     
                        predecesseurs[succ] = sommet
                        updated = True
            if not updated :
                break
            
            # print(f"Distance a l'iteration {i}: {distances}")
            # i+=1
        
        #Détection des cycles négatifs
        for sommet in G :
            for (cout, succ) in G[sommet] :
                if distances[sommet] + cout < distances[succ] : 
                    return 'INVALID - negative cycle detected'

        return distances, predecesseurs


def main():
    source = 'S'

    G = make_graph()
    shortest_paths, predecesseurs = bellman_ford(G, source)
    print(f'plus court chemin de {source}: {shortest_paths}\nListe de predecesseurs de {source}: {predecesseurs}')

    G = make_graph_with_negative_cycle()
    #negative_cycle = bellman_ford(G, source)
    #print(f'Shortest path from {source}: {negative_cycle}')


main()
