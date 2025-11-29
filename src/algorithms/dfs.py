def dfs(graph, start_id):
    """
    Depth-First Search (DFS)
    Returns the order of visited nodes starting from start_id.
    """
    start_id = int(start_id)
    if start_id not in graph.nodes:
        raise ValueError("Start node does not exist.")

    visited = []
    stack = [start_id]
    seen = set()

    while stack:
        current = stack.pop()

        if current in seen:
            continue

        seen.add(current)
        visited.append(current)

        # Add neighbors in reverse sorted order 
        # so that the smallest neighbor is processed first
        for neighbor in sorted(graph.get_neighbors(current), reverse=True):
            if neighbor not in seen:
                stack.append(neighbor)

    return visited
