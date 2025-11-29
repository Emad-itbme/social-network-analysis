def welsh_powell(graph):
    """
    Welsh–Powell graph coloring algorithm.
    Returns a dictionary: {node_id: color_index}.
    """

    # Step 1: sort nodes by degree (descending)
    nodes_sorted = sorted(
        graph.nodes.keys(),
        key=lambda nid: len(graph.get_neighbors(nid)),
        reverse=True
    )

    color_of = {}  # node_id -> assigned color

    # Step 2: assign colors
    for node in nodes_sorted:
        # find used colors among neighbors
        neighbor_colors = {color_of[n] for n in graph.get_neighbors(node) if n in color_of}

        # find the lowest available color
        color = 0
        while color in neighbor_colors:
            color += 1

        color_of[node] = color

    return color_of
