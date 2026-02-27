import time
import matplotlib.pyplot as plt
import random

from grapheRandom import generer_graphe
from dijkstra import *
from dijkstra_tas import *
from Bellman_Ford import *


def compare_dijkstra_BellmanFord():
    sizes = [50, 100, 150, 200, 300, 500, 700, 1000]  # tailles de graphes à tester
    results = []
    random.seed(42)
    times_no_heap = []
    times_with_heap = []
    times_bellman = []
   
    for n in sizes:
        p = 0.8
        nodes = list(range(n))  # sommets = entiers
        graph = generer_graphe(n, p=p, pondere=False, poids_min=1, poids_max=10, alphabetique=False)  
        start = nodes[0]

        # Dijkstra sans tas
        t0 = time.time()
        dijkstra(graph, start)
        t_no_heap = time.time() - t0

        # Dijkstra avec tas
        t0 = time.time()
        dijkstra_avec_tas(graph, start)
        t_with_heap = time.time() - t0

        # Bellman-Ford 
        t0 = time.time()
        bellman_ford(graph, start)
        t_bellman = time.time() - t0

        # Stocker les résultats
        times_no_heap.append(t_no_heap)
        times_with_heap.append(t_with_heap)
        times_bellman.append(t_bellman)
        results.append((n, t_no_heap, t_with_heap, t_bellman))

        print(f"n={n} | p ={p} Sans tas: {t_no_heap:.4f}s | Avec tas: {t_with_heap:.4f}s | Bellman-Ford: {t_bellman:.4f}s")

    # Affichage du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_no_heap, label="Dijkstra sans tas", marker='o', color='red')
    plt.plot(sizes, times_with_heap, label="Dijkstra avec tas (heapq)", marker='o', color='blue')
    plt.plot(sizes, times_bellman, label="Bellman-Ford", marker='*', color='green')
    plt.xlabel("Nombre de sommets")
    plt.ylabel("Temps d'exécution (secondes)")
    plt.title(f"Comparaison des algorithmes de plus court chemin (p = {p}) ")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    #plt.savefig("comparer_N_0.1.png", dpi=300)
    plt.show()
    
    return results

compare_dijkstra_BellmanFord()
