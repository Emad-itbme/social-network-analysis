from .node import Node
from .edge import Edge


class Graph:
    """
    Represents the whole social network as an undirected weighted graph.

    Internal structure:
    - nodes: dict[int, Node]
    - edges: dict[tuple[int, int], Edge]   # key is (min(u, v), max(u, v))
    - adjacency: dict[int, set[int]]       # node_id -> neighbor IDs
    """

    def __init__(self):
        self.nodes: dict[int, Node] = {}
        self.edges: dict[tuple[int, int], Edge] = {}
        self.adjacency: dict[int, set[int]] = {}

    # ------------------------------------------------------------------
    # Node operations
    # ------------------------------------------------------------------

    def add_node(
        self,
        node_id: int,
        name: str | None = None,
        activity: float = 0.0,
        interaction: int = 0,
        connection_count: int = 0,
    ) -> Node:
        """
        Create and add a new node to the graph.
        Raises ValueError if a node with the same ID already exists.
        """
        node_id = int(node_id)
        if node_id in self.nodes:
            raise ValueError(f"Node with ID {node_id} already exists.")

        node = Node(
            node_id=node_id,
            name=name,
            activity=activity,
            interaction=interaction,
            connection_count=connection_count,
        )

        self.nodes[node_id] = node
        self.adjacency[node_id] = set()
        return node

    def add_node_object(self, node: Node) -> None:
        """
        Add an existing Node instance to the graph.
        Useful when nodes are created elsewhere (e.g., CSV loader).
        """
        if node.id in self.nodes:
            raise ValueError(f"Node with ID {node.id} already exists.")

        self.nodes[node.id] = node
        self.adjacency[node.id] = set()

    def update_node(
        self,
        node_id: int,
        name: str | None = None,
        activity: float | None = None,
        interaction: int | None = None,
        connection_count: int | None = None,
    ) -> None:
        """Update basic attributes of a node."""
        node_id = int(node_id)
        if node_id not in self.nodes:
            raise ValueError("Node not found.")

        node = self.nodes[node_id]
        if name is not None:
            node.name = name
        if activity is not None:
            node.activity = float(activity)
        if interaction is not None:
            node.interaction = int(interaction)
        if connection_count is not None:
            node.connection_count = int(connection_count)

    def remove_node(self, node_id: int) -> None:
        """
        Remove a node and all its incident edges from the graph.
        """
        node_id = int(node_id)
        if node_id not in self.nodes:
            raise ValueError("Node not found.")

        # Remove all edges connected to this node
        neighbors = list(self.adjacency.get(node_id, []))
        for neighbor in neighbors:
            self.remove_edge(node_id, neighbor)

        # Remove node itself
        del self.nodes[node_id]
        del self.adjacency[node_id]

    # ------------------------------------------------------------------
    # Edge operations
    # ------------------------------------------------------------------

    def _edge_key(self, u: int, v: int) -> tuple[int, int]:
        """Return a canonical key for an undirected edge."""
        u = int(u)
        v = int(v)
        if u == v:
            raise ValueError("Self-loops are not allowed.")
        return (u, v) if u < v else (v, u)

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> Edge:
        """
        Add an undirected edge between nodes u and v.
        Raises ValueError if one of the nodes does not exist.
        """
        u = int(u)
        v = int(v)

        if u not in self.nodes or v not in self.nodes:
            raise ValueError("Both nodes must exist before adding an edge.")

        key = self._edge_key(u, v)
        if key in self.edges:
            # If edge already exists, just update the weight
            self.edges[key].weight = float(weight)
            return self.edges[key]

        edge = Edge(u, v, weight)
        self.edges[key] = edge

        # Update adjacency and neighbors
        self.adjacency[u].add(v)
        self.adjacency[v].add(u)
        self.nodes[u].add_neighbor(v)
        self.nodes[v].add_neighbor(u)

        return edge

    def update_edge_weight(self, u: int, v: int, weight: float) -> None:
        """Update the weight of an existing edge."""
        key = self._edge_key(u, v)
        if key not in self.edges:
            raise ValueError("Edge does not exist.")
        self.edges[key].weight = float(weight)

    def remove_edge(self, u: int, v: int) -> None:
        """Remove an edge between u and v, if it exists."""
        u = int(u)
        v = int(v)
        key = self._edge_key(u, v)
        if key not in self.edges:
            return  # silently ignore if edge does not exist

        del self.edges[key]

        # Update adjacency and neighbors
        if u in self.adjacency:
            self.adjacency[u].discard(v)
        if v in self.adjacency:
            self.adjacency[v].discard(u)

        if u in self.nodes:
            self.nodes[u].remove_neighbor(v)
        if v in self.nodes:
            self.nodes[v].remove_neighbor(u)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get_neighbors(self, node_id: int) -> set[int]:
        """Return the neighbor IDs of a given node."""
        return set(self.adjacency.get(int(node_id), set()))

    def has_edge(self, u: int, v: int) -> bool:
        """Check if there is an edge between u and v."""
        return self._edge_key(u, v) in self.edges

    def get_edge_weight(self, u: int, v: int) -> float | None:
        """Return the weight of edge (u, v), or None if no edge exists."""
        key = self._edge_key(u, v)
        edge = self.edges.get(key)
        return edge.weight if edge is not None else None

    def get_nodes(self) -> list[Node]:
        """Return all nodes as a list."""
        return list(self.nodes.values())

    def get_edges(self) -> list[Edge]:
        """Return all edges as a list."""
        return list(self.edges.values())

    def clear(self) -> None:
        """Remove all nodes and edges from the graph."""
        self.nodes.clear()
        self.edges.clear()
        self.adjacency.clear()
