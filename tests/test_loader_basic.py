import sys, os
sys.path.append(os.path.abspath("src"))

from models.graph_loader import GraphLoader

graph = GraphLoader.load_from_csv("data/sample_small.csv")

print("Nodes:", graph.get_nodes())
print("Edges:", graph.get_edges())
print("Adjacency:", graph.adjacency)
