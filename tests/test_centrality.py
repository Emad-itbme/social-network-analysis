import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.degree_centrality import degree_centrality
from models.graph_loader import GraphLoader

csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")
graph = GraphLoader.load_from_csv(csv_path)

centrality = degree_centrality(graph, top_n=5)

print("Top 5 nodes by degree:")
for node_id, degree in centrality:
    print(f"Node {node_id}: degree = {degree}")
