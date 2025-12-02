import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.dijkstra import dijkstra, reconstruct_path
from models.graph_loader import GraphLoader

csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")
graph = GraphLoader.load_from_csv(csv_path)

distances, previous = dijkstra(graph, start_id=1)

print("Distances from node 1:")
for node, d in distances.items():
    print(f"{node}: {d}")

print("\nShortest path from 1 to 10:")
print(reconstruct_path(previous, 1, 10))
