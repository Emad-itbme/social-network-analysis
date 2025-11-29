import heapq

def heuristic(u, v):
    """
    A* heuristic function.
    Since we do not have spatial coordinates,
    we use a zero heuristic (this reduces to Dijkstra).
    """
    return 0.0


def astar(graph, start_id, target_id):
    """
    A* shortest path algorithm.
    Returns:
    - distances: dict[node -> cost]
    - previous: dict[node -> parent]
    - path: reconstructed shortest path
    """

    start_id = int(start_id)
    target_id = int(target_id)

    if start_id not in graph.nodes or target_id not in graph.nodes:
        raise ValueError("Start or target node does not exist.")

    distances = {nid: float("inf") for nid in graph.nodes}
    previous = {nid: None for nid in graph.nodes}
    distances[start_id] = 0.0

    pq = [(0.0, start_id)]

    while pq:
        current_f, u = heapq.heappop(pq)

        if u == target_id:
            break

        for v in graph.get_neighbors(u):
            g_cost = distances[u] + graph.get_edge_weight(u, v)
            h_cost = heuristic(v, target_id)
            f_cost = g_cost + h_cost

            if g_cost < distances[v]:
                distances[v] = g_cost
                previous[v] = u
                heapq.heappush(pq, (f_cost, v))

    # reconstruct path
    return distances, previous, reconstruct_path(previous, start_id, target_id)


def reconstruct_path(previous, start_id, target_id):
    """Reconstruct path from start to target."""
    path = []
    current = target_id

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if not path or path[0] != start_id:
        return []

    return path
