import time
import matplotlib.pyplot as plt
import random

from grapheRandom import generer_graphe
from dijkstra import *
from dijkstra_tas import *
from Bellman_Ford import *


def compare_densite(n=500, p_values=None):
    if p_values is None:
        p_values = [0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
    n = 500
    random.seed(42)

    results = []
    times_no_heap = []
    times_with_heap = []
    times_bellman = []

    def format_time(t):
        return f"{t:.4f}s" if t is not None else "Erreur"

    for p in p_values:
        print(f"Test densité p={p:.2f} avec n={n} sommets...")
        graph = generer_graphe(n, p=p, pondere=False, alphabetique=False)
        start = 0

        try:
            t0 = time.time()
            dijkstra(graph, start)
            t_no_heap = time.time() - t0
        except Exception as e:
            print("Erreur Dijkstra sans tas:", e)
            t_no_heap = None

        try:
            t0 = time.time()
            dijkstra_avec_tas(graph, start)
            t_with_heap = time.time() - t0
        except Exception as e:
            print("Erreur Dijkstra avec tas:", e)
            t_with_heap = None

        try:
            t0 = time.time()
            bellman_ford(graph, start)
            t_bellman = time.time() - t0
        except Exception as e:
            print("Erreur Bellman-Ford:", e)
            t_bellman = None

        times_no_heap.append(t_no_heap)
        times_with_heap.append(t_with_heap)
        times_bellman.append(t_bellman)
        results.append((n, p, t_no_heap, t_with_heap, t_bellman))

        print(f"Résultats: Sans tas={format_time(t_no_heap)} | Avec tas={format_time(t_with_heap)} | Bellman-Ford={format_time(t_bellman)}\n")
    
    # Affichage du graphique
    plt.figure(figsize=(10, 6))
    plt.plot(p_values, times_no_heap, label="Dijkstra sans tas", marker='o', color='red')
    plt.plot(p_values, times_with_heap, label="Dijkstra avec tas (heapq)", marker='o', color='blue')
    plt.plot(p_values, times_bellman, label="Bellman-Ford", marker='*', color='green')
    plt.xlabel("Densité (probabilité d'arête p)")
    plt.ylabel("Temps d'exécution (secondes)")
    plt.title(f"Comparaison des algorithmes de plus court chemin (n = {n})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    #plt.savefig("Dijk_A_S_Bellm_densite n 500.png", dpi=300)
    plt.show()
    
    return results

compare_densite(n=200, p_values=None)
