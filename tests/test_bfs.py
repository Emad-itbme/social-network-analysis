import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.bfs import bfs
from models.graph_loader import GraphLoader

csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")
graph = GraphLoader.load_from_csv(csv_path)

print("BFS from node 1:", bfs(graph, 1))
