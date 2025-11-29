from collections import deque

def bfs(graph, start_id):
    """
    Breadth-First Search (BFS)
    Returns the order of visited nodes starting from start_id.
    """

    start_id = int(start_id)
    if start_id not in graph.nodes:
        raise ValueError("Start node does not exist.")

    visited = []
    queue = deque([start_id])
    seen = set([start_id])

    while queue:
        current = queue.popleft()
        visited.append(current)

        # Process neighbors in sorted order for consistent output
        for neighbor in sorted(graph.get_neighbors(current)):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)

    return visited
