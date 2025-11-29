class Edge:
    """
    Represents an undirected edge between two nodes in the graph.
    - u: ID of the first endpoint
    - v: ID of the second endpoint
    - weight: numeric weight calculated from node features
    """

    def __init__(self, u: int, v: int, weight: float = 1.0):
        if u == v:
            raise ValueError("Self-loops are not allowed (u and v cannot be equal).")

        # Ensure IDs are stored as integers
        self.u = int(u)
        self.v = int(v)
        self.weight = float(weight)

    def __repr__(self) -> str:
        return f"Edge({self.u} -- {self.v}, weight={self.weight})"

    def key(self):
        """
        Returns a canonical key for this undirected edge.
        This is useful for storing edges in dictionaries without duplicates.
        """
        return tuple(sorted((self.u, self.v)))
