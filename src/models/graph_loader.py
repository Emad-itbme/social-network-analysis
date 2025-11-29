import csv
import math
from .graph import Graph
from .node import Node


class GraphLoader:
    """
    Loads a social network graph from a CSV file and calculates edge weights
    using the required formula.
    """

    @staticmethod
    def load_from_csv(path: str) -> Graph:
        """
        Load nodes and edges from a CSV file.
        Expected CSV columns:
        - DugumId
        - Aktiflik
        - Etkilesim
        - Baglanti
        - Komsular  (comma-separated neighbor IDs)
        """

        graph = Graph()
        temp_neighbors = {}  # store neighbor lists temporarily

        # ---------------------------------------------------------
        # Step 1: Load nodes
        # ---------------------------------------------------------
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                node_id = int(row["DugumId"])
                activity = float(row["Aktiflik"])
                interaction = float(row["Etkilesim"])
                connection_count = float(row["Baglanti"])

                # Create Node
                node = Node(
                    node_id=node_id,
                    activity=activity,
                    interaction=interaction,
                    connection_count=connection_count,
                )
                graph.add_node_object(node)

                # Store neighbors for later
                neighbors_str = row["Komsular"]
                neighbors = []
                if neighbors_str.strip():
                    neighbors = [int(x) for x in neighbors_str.split(",")]

                temp_neighbors[node_id] = neighbors

        # ---------------------------------------------------------
        # Step 2: Add edges + calculate weights
        # ---------------------------------------------------------
        for u, neighbors in temp_neighbors.items():
            for v in neighbors:
                if u < v:  # to avoid duplicate edges in undirected graph
                    n1 = graph.nodes[u]
                    n2 = graph.nodes[v]

                    # Weight formula
                    weight = 1.0 / (
                        1.0
                        + math.sqrt(
                            (n1.activity - n2.activity) ** 2
                            + (n1.interaction - n2.interaction) ** 2
                            + (n1.connection_count - n2.connection_count) ** 2
                        )
                    )

                    graph.add_edge(u, v, weight)

        return graph
