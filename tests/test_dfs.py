import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.dfs import dfs
from models.graph_loader import GraphLoader

# Absolute path to CSV
csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")

graph = GraphLoader.load_from_csv(csv_path)

print("DFS from node 1:", dfs(graph, 1))
print("DFS from node 3:", dfs(graph, 3))
