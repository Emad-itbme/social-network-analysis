import sys, os
sys.path.append(os.path.abspath("src"))

from algorithms.connected_components import connected_components
from models.graph_loader import GraphLoader

csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_small.csv")
graph = GraphLoader.load_from_csv(csv_path)

components = connected_components(graph)

print("Connected Components:")
for comp in components:
    print(comp)
