import sys
import os

sys.path.append(os.path.abspath("src"))

from models.graph import Graph


# Create a graph instance
g = Graph()

# Add nodes
g.add_node(1, name="Alice", activity=0.8, interaction=12, connection_count=3)
g.add_node(2, name="Bob", activity=0.5, interaction=8, connection_count=2)
g.add_node(3, name="Charlie", activity=0.3, interaction=5, connection_count=1)

# Add edges
g.add_edge(1, 2, weight=2.5)
g.add_edge(2, 3, weight=1.2)

print("Nodes:")
for n in g.get_nodes():
    print(n)

print("\nEdges:")
for e in g.get_edges():
    print(e)

print("\nAdjacency list:", g.adjacency)

# Test neighbor retrieval
print("\nNeighbors of 2:", g.get_neighbors(2))

# Test updating node
g.update_node(3, name="Charlie Updated", activity=0.9)
print("\nUpdated node 3:", g.nodes[3])

# Test edge weight update
g.update_edge_weight(1, 2, 9.99)
print("\nUpdated edge weight (1-2):", g.get_edge_weight(1, 2))

# Remove edge
g.remove_edge(2, 3)
print("\nEdges after removing (2-3):", g.get_edges())

# Remove node
g.remove_node(1)
print("\nNodes after removing 1:", g.get_nodes())
print("Adjacency after removing 1:", g.adjacency)
