class Node:
    """
    Represents a single node (user) in the social network graph.
    Each node has:
    - id: unique identifier
    - name: optional label (user name)
    - activity: numeric feature from CSV
    - interaction: numeric feature from CSV
    - connection_count: numeric feature from CSV
    - neighbors: a set of neighbor node IDs
    """

    def __init__(self, node_id, name=None, activity=0.0, interaction=0, connection_count=0):
        self.id = int(node_id)
        self.name = name or f"User {self.id}"
        self.activity = float(activity)
        self.interaction = int(interaction)
        self.connection_count = int(connection_count)
        self.neighbors = set()  # will be filled when edges are added

    def add_neighbor(self, neighbor_id: int) -> None:
        """Add a neighbor ID to this node."""
        self.neighbors.add(int(neighbor_id))

    def remove_neighbor(self, neighbor_id: int) -> None:
        """Remove a neighbor ID from this node if present."""
        self.neighbors.discard(int(neighbor_id))

    def __repr__(self) -> str:
        return f"Node(id={self.id}, name={self.name})"
