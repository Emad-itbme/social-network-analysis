import csv
import json
import math
from typing import Callable, Dict, List, Optional, Tuple, Any
from .graph import Graph
from .node import Node


class GraphLoader:
    """
    A generalized and extensible loader for social network graphs from multiple formats.
    
    Supports:
    - CSV files with customizable column mappings
    - JSON files
    - Custom weight calculation formulas
    - Node attribute specifications
    """

    # Default column mappings for CSV files
    DEFAULT_CSV_COLUMNS = {
        "node_id": "DugumId",
        "activity": "Aktiflik",
        "interaction": "Etkilesim",
        "connection_count": "Baglanti",
        "neighbors": "Komsular",
    }

    @staticmethod
    def load_from_csv(
        path: str,
        column_mapping: Optional[Dict[str, str]] = None,
        weight_formula: Optional[Callable] = None,
        encoding: str = "utf-8",
    ) -> Graph:
        """
        Load nodes and edges from a CSV file with customizable column mappings.

        Args:
            path: Path to the CSV file
            column_mapping: Dict mapping internal names to CSV column names.
                           If None, uses DEFAULT_CSV_COLUMNS.
                           Required keys: 'node_id', 'neighbors'
                           Optional keys: 'activity', 'interaction', 'connection_count', and any custom attributes
            weight_formula: Callable(node1: Node, node2: Node) -> float
                           If None, uses default Euclidean distance formula
            encoding: File encoding (default: utf-8)

        Returns:
            Graph object with nodes and edges loaded
        """
        if column_mapping is None:
            column_mapping = GraphLoader.DEFAULT_CSV_COLUMNS

        graph = Graph()
        temp_neighbors = {}

        # ---------------------------------------------------------
        # Step 1: Load nodes
        # ---------------------------------------------------------
        with open(path, "r", encoding=encoding) as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    node_id = int(row[column_mapping["node_id"]])
                except (KeyError, ValueError) as e:
                    raise ValueError(f"Failed to read node_id from row: {row}") from e

                # Build node attributes
                node_attrs = {"node_id": node_id}

                # Read optional attributes
                for attr_key in ["activity", "interaction", "connection_count"]:
                    if attr_key in column_mapping:
                        try:
                            col_name = column_mapping[attr_key]
                            if col_name in row and row[col_name].strip():
                                node_attrs[attr_key] = float(row[col_name])
                        except ValueError:
                            pass  # Skip if conversion fails

                # Read any additional custom attributes
                for key, col_name in column_mapping.items():
                    if key not in ["node_id", "activity", "interaction", "connection_count", "neighbors"]:
                        if col_name in row and row[col_name].strip():
                            try:
                                node_attrs[key] = float(row[col_name])
                            except ValueError:
                                node_attrs[key] = row[col_name]  # Store as string if not numeric

                # Create Node
                node = Node(**node_attrs)
                graph.add_node_object(node)

                # Store neighbors for later
                if "neighbors" in column_mapping:
                    neighbors_str = row[column_mapping["neighbors"]]
                    neighbors = []
                    if neighbors_str.strip():
                        neighbors = [int(x) for x in neighbors_str.split(",")]
                    temp_neighbors[node_id] = neighbors

        # ---------------------------------------------------------
        # Step 2: Add edges + calculate weights
        # ---------------------------------------------------------
        default_weight_fn = weight_formula or GraphLoader._default_weight_formula
        
        for u, neighbors in temp_neighbors.items():
            for v in neighbors:
                if u < v:  # Avoid duplicate edges in undirected graph
                    n1 = graph.nodes[u]
                    n2 = graph.nodes[v]
                    weight = default_weight_fn(n1, n2)
                    graph.add_edge(u, v, weight)

        return graph

    @staticmethod
    def load_from_json(
        path: str,
        weight_formula: Optional[Callable] = None,
        encoding: str = "utf-8",
    ) -> Graph:
        """
        Load nodes and edges from a JSON file.

        JSON structure expected:
        {
            "nodes": [
                {"id": 1, "activity": 0.8, "interaction": 12, "connection_count": 5, ...},
                ...
            ],
            "edges": [
                {"source": 1, "target": 2, "weight": 0.5},
                ...
            ]
        }

        Args:
            path: Path to the JSON file
            weight_formula: Custom weight calculation function (not used if weights are in JSON)
            encoding: File encoding

        Returns:
            Graph object with nodes and edges loaded
        """
        with open(path, "r", encoding=encoding) as f:
            data = json.load(f)

        graph = Graph()

        # Load nodes
        for node_data in data.get("nodes", []):
            node = Node(**node_data)
            graph.add_node_object(node)

        # Load edges
        default_weight_fn = weight_formula or GraphLoader._default_weight_formula
        
        for edge_data in data.get("edges", []):
            u = edge_data["source"]
            v = edge_data["target"]
            
            # Use provided weight or calculate
            if "weight" in edge_data:
                weight = edge_data["weight"]
            else:
                n1 = graph.nodes[u]
                n2 = graph.nodes[v]
                weight = default_weight_fn(n1, n2)
            
            graph.add_edge(u, v, weight)

        return graph

    @staticmethod
    def _default_weight_formula(node1: Node, node2: Node) -> float:
        """
        Default weight formula based on Euclidean distance of node attributes.
        
        weight = 1 / (1 + sqrt(sum of squared differences))
        """
        activity_diff = (node1.activity - node2.activity) ** 2
        interaction_diff = (node1.interaction - node2.interaction) ** 2
        connection_diff = (node1.connection_count - node2.connection_count) ** 2
        
        distance = math.sqrt(activity_diff + interaction_diff + connection_diff)
        return 1.0 / (1.0 + distance)

    @staticmethod
    def create_custom_weight_formula(
        attribute_names: List[str],
        weights: Optional[List[float]] = None,
    ) -> Callable:
        """
        Create a custom weight formula based on specified node attributes.

        Args:
            attribute_names: List of node attribute names to use (e.g., ['activity', 'interaction'])
            weights: Optional list of weights for each attribute (default: equal weights)

        Returns:
            A callable weight function
        """
        if weights is None:
            weights = [1.0] * len(attribute_names)

        if len(weights) != len(attribute_names):
            raise ValueError("weights and attribute_names must have the same length")

        def custom_formula(node1: Node, node2: Node) -> float:
            distance_sq = 0.0
            for attr, weight in zip(attribute_names, weights):
                val1 = getattr(node1, attr, 0.0)
                val2 = getattr(node2, attr, 0.0)
                distance_sq += weight * ((val1 - val2) ** 2)
            
            distance = math.sqrt(distance_sq)
            return 1.0 / (1.0 + distance)

        return custom_formula
