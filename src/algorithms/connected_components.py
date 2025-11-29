def connected_components(graph):
    """
    Finds all connected components in an undirected graph.
    Returns a list of components, each component is a list of node IDs.
    """

    visited = set()
    components = []

    for node_id in graph.nodes:
        if node_id not in visited:
            # Start BFS/DFS from this node
            component = []
            stack = [node_id]

            while stack:
                u = stack.pop()
                if u in visited:
                    continue

                visited.add(u)
                component.append(u)

                for neighbor in graph.get_neighbors(u):
                    if neighbor not in visited:
                        stack.append(neighbor)

            components.append(sorted(component))

    return components
