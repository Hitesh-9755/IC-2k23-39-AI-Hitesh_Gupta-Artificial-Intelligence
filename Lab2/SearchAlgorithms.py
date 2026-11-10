"""
Heuristic & Uninformed Search Algorithms
=========================================
Implements five search strategies on a weighted graph:

    - Breadth-First Search (BFS)
    - Depth-First Search (DFS)
    - Hill Climbing
    - Best-First Search
    - A* Search

Each function returns (path, nodes_expanded, time_taken) so the
algorithms can be compared.
"""

import heapq
import time
from collections import deque


def reconstruct_path(parent, start, goal):
    """Rebuild the path from start to goal using the parent map."""
    if goal not in parent:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


# ---------------------------------------------------------------------------
# Uninformed searches
# ---------------------------------------------------------------------------

def bfs(graph, start, goal):
    """Breadth-First Search using a FIFO queue."""
    t0 = time.perf_counter()
    queue = deque([start])
    parent = {start: None}
    expanded = 0

    while queue:
        node = queue.popleft()
        expanded += 1
        if node == goal:
            return reconstruct_path(parent, start, goal), expanded, \
                time.perf_counter() - t0
        for nbr, _ in graph.get(node, []):
            if nbr not in parent:
                parent[nbr] = node
                queue.append(nbr)
    return None, expanded, time.perf_counter() - t0


def dfs(graph, start, goal):
    """Depth-First Search using a LIFO stack."""
    t0 = time.perf_counter()
    stack = [start]
    parent = {start: None}
    expanded = 0

    while stack:
        node = stack.pop()
        expanded += 1
        if node == goal:
            return reconstruct_path(parent, start, goal), expanded, \
                time.perf_counter() - t0
        for nbr, _ in graph.get(node, []):
            if nbr not in parent:
                parent[nbr] = node
                stack.append(nbr)
    return None, expanded, time.perf_counter() - t0


# ---------------------------------------------------------------------------
# Informed searches
# ---------------------------------------------------------------------------

def hill_climbing(graph, start, goal, heuristic):
    """Hill climbing: move to the neighbour with the lowest h.

    No backtracking, so it can get stuck in a local minimum.
    """
    t0 = time.perf_counter()
    current = start
    path = [start]
    expanded = 0
    visited = {start}

    while current != goal:
        expanded += 1
        neighbors = [n for n, _ in graph.get(current, [])
                     if n not in visited]
        if not neighbors:
            return None, expanded, time.perf_counter() - t0
        best = min(neighbors, key=heuristic)
        if heuristic(best) >= heuristic(current):
            # local minimum - stuck
            return None, expanded, time.perf_counter() - t0
        visited.add(best)
        path.append(best)
        current = best

    return path, expanded, time.perf_counter() - t0


def best_first(graph, start, goal, heuristic):
    """Greedy Best-First Search: expand node with lowest h(n)."""
    t0 = time.perf_counter()
    open_heap = [(heuristic(start), start)]
    parent = {start: None}
    expanded = 0

    while open_heap:
        _, node = heapq.heappop(open_heap)
        expanded += 1
        if node == goal:
            return reconstruct_path(parent, start, goal), expanded, \
                time.perf_counter() - t0
        for nbr, _ in graph.get(node, []):
            if nbr not in parent:
                parent[nbr] = node
                heapq.heappush(open_heap, (heuristic(nbr), nbr))
    return None, expanded, time.perf_counter() - t0


def astar(graph, start, goal, heuristic):
    """A* Search: f(n) = g(n) + h(n)."""
    t0 = time.perf_counter()
    open_heap = [(heuristic(start), 0.0, start)]
    g_score = {start: 0.0}
    parent = {start: None}
    expanded = 0

    while open_heap:
        _, g, node = heapq.heappop(open_heap)
        if node == goal:
            return reconstruct_path(parent, start, goal), expanded, \
                time.perf_counter() - t0
        expanded += 1
        for nbr, cost in graph.get(node, []):
            tentative_g = g + cost
            if nbr not in g_score or tentative_g < g_score[nbr]:
                g_score[nbr] = tentative_g
                parent[nbr] = node
                f = tentative_g + heuristic(nbr)
                heapq.heappush(open_heap, (f, tentative_g, nbr))
    return None, expanded, time.perf_counter() - t0


# ---------------------------------------------------------------------------
# Demo: route planning graph
# ---------------------------------------------------------------------------

def build_route_graph():
    """A small weighted graph of city-to-city distances."""
    edges = [
        ("Arad", "Zerind", 75), ("Arad", "Sibiu", 140),
        ("Arad", "Timisoara", 118),
        ("Zerind", "Oradea", 71),
        ("Oradea", "Sibiu", 151), ("Oradea", "Fagaras", 99),
        ("Sibiu", "Fagaras", 99), ("Sibiu", "RimnicuVilcea", 80),
        ("Timisoara", "Lugoj", 111),
        ("Lugoj", "Mehadia", 70), ("Mehadia", "Drobeta", 75),
        ("Drobeta", "Craiova", 120),
        ("Craiova", "RimnicuVilcea", 146), ("Craiova", "Pitesti", 138),
        ("RimnicuVilcea", "Pitesti", 97),
        ("Pitesti", "Bucharest", 101),
        ("Fagaras", "Bucharest", 211),
    ]
    graph = {}
    for a, b, w in edges:
        graph.setdefault(a, []).append((b, w))
        graph.setdefault(b, []).append((a, w))
    return graph


def main():
    graph = build_route_graph()
    start, goal = "Arad", "Bucharest"

    # Straight-line distances to Bucharest (admissible heuristic)
    h_dist = {
        "Arad": 366, "Zerind": 374, "Oradea": 380, "Sibiu": 253,
        "Fagaras": 176, "RimnicuVilcea": 193, "Timisoara": 329,
        "Lugoj": 244, "Mehadia": 241, "Drobeta": 242,
        "Craiova": 160, "Pitesti": 100, "Bucharest": 0,
    }
    heuristic = lambda node: h_dist.get(node, float("inf"))

    algorithms = [
        ("BFS", lambda: bfs(graph, start, goal)),
        ("DFS", lambda: dfs(graph, start, goal)),
        ("Hill Climbing", lambda: hill_climbing(graph, start, goal,
                                                heuristic)),
        ("Best-First", lambda: best_first(graph, start, goal, heuristic)),
        ("A*", lambda: astar(graph, start, goal, heuristic)),
    ]

    print("Route planning: %s -> %s\n" % (start, goal))
    print("%-15s %11s %7s %10s" % ("Algorithm", "Path Length",
                                   "Nodes", "Time (ms)"))
    print("-" * 48)
    for name, fn in algorithms:
        path, expanded, elapsed = fn()
        length = len(path) - 1 if path else "FAIL"
        print("%-15s %11s %7d %10.3f" % (name, length, expanded,
                                         elapsed * 1000))
        if path:
            print("    Path: " + " -> ".join(path))


if __name__ == "__main__":
    main()
