import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.welsh_powell import welsh_powell
from models.graph_loader import GraphLoader

csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")
graph = GraphLoader.load_from_csv(csv_path)

coloring = welsh_powell(graph)

print("Node colors:")
for node_id, color in sorted(coloring.items()):
    print(f"Node {node_id}: Color {color}")
