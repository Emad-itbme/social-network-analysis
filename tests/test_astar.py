import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.astar import astar
from models.graph_loader import GraphLoader

csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")
graph = GraphLoader.load_from_csv(csv_path)

distances, previous, path = astar(graph, 1, 10)

print("A* distances from node 1:")
for node, d in distances.items():
    print(f"{node}: {d}")

print("\nShortest path from 1 to 10 (A*):")
print(path)
