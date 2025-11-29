def degree_centrality(graph, top_n=5):
    """
    Computes degree centrality for each node.
    Returns a list of tuples (node_id, degree) sorted by degree descending.
    """

    degrees = []

    for node_id, node in graph.nodes.items():
        degree = len(graph.get_neighbors(node_id))
        degrees.append((node_id, degree))

    # Sort by degree (descending), then by node ID (ascending)
    degrees.sort(key=lambda x: (-x[1], x[0]))

    return degrees[:top_n]
