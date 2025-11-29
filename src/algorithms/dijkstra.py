import heapq

def dijkstra(graph, start_id):
    """
    Dijkstra shortest path algorithm.
    Returns:
    - distances: dict[node_id -> shortest distance]
    - previous: dict[node_id -> previous node for path reconstruction]
    """

    start_id = int(start_id)
    if start_id not in graph.nodes:
        raise ValueError("Start node does not exist.")

    # Initialize distances and previous node map
    distances = {node_id: float("inf") for node_id in graph.nodes}
    previous = {node_id: None for node_id in graph.nodes}
    distances[start_id] = 0.0

    # Min-heap priority queue
    pq = [(0.0, start_id)]

    while pq:
        current_dist, u = heapq.heappop(pq)

        # Skip outdated entries
        if current_dist > distances[u]:
            continue

        # Relaxation step
        for v in graph.get_neighbors(u):
            weight = graph.get_edge_weight(u, v)
            new_dist = current_dist + weight

            if new_dist < distances[v]:
                distances[v] = new_dist
                previous[v] = u
                heapq.heappush(pq, (new_dist, v))

    return distances, previous


def reconstruct_path(previous, start_id, target_id):
    """
    Reconstruct the shortest path using the 'previous' dictionary.
    Returns a list of node IDs representing the path.
    """

    path = []
    current = target_id

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    # Verify the path starts from the start node
    if path[0] != start_id:
        return []  # no valid path

    return path
