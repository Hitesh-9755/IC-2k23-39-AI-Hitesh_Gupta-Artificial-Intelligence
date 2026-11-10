"""
Maze Solver
===========
Solves a grid maze using BFS, DFS, and A* search.

Maze legend:
    '#'  wall
    '.'  open path
    'S'  start
    'G'  goal
"""

import heapq
import time
from collections import deque

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # L, R, U, D


def find_cell(maze, target):
    """Locate the (row, col) of a special cell in the maze."""
    for r, row in enumerate(maze):
        for c, ch in enumerate(row):
            if ch == target:
                return (r, c)
    raise ValueError("Cell '%s' not found in maze" % target)


def is_walkable(maze, cell):
    """Return True if the cell is inside bounds and not a wall."""
    r, c = cell
    return (0 <= r < len(maze)
            and 0 <= c < len(maze[0])
            and maze[r][c] != "#")


def neighbors(maze, cell):
    """Return walkable neighbour cells."""
    r, c = cell
    result = []
    for dr, dc in DIRECTIONS:
        nxt = (r + dr, c + dc)
        if is_walkable(maze, nxt):
            result.append(nxt)
    return result


def manhattan(a, b):
    """Manhattan distance heuristic for grid worlds."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct(parent, start, goal):
    """Rebuild cell path from parent map."""
    if goal not in parent:
        return None
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


# ---------------------------------------------------------------------------
# Search algorithms
# ---------------------------------------------------------------------------

def bfs_maze(maze, start, goal):
    """BFS maze solver - guarantees shortest path."""
    t0 = time.perf_counter()
    queue = deque([start])
    parent = {start: None}
    expanded = 0
    while queue:
        node = queue.popleft()
        expanded += 1
        if node == goal:
            return reconstruct(parent, start, goal), expanded, \
                time.perf_counter() - t0
        for nxt in neighbors(maze, node):
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)
    return None, expanded, time.perf_counter() - t0


def dfs_maze(maze, start, goal):
    """DFS maze solver - may find a longer path than BFS."""
    t0 = time.perf_counter()
    stack = [start]
    parent = {start: None}
    expanded = 0
    while stack:
        node = stack.pop()
        expanded += 1
        if node == goal:
            return reconstruct(parent, start, goal), expanded, \
                time.perf_counter() - t0
        for nxt in neighbors(maze, node):
            if nxt not in parent:
                parent[nxt] = node
                stack.append(nxt)
    return None, expanded, time.perf_counter() - t0


def astar_maze(maze, start, goal):
    """A* maze solver using Manhattan distance heuristic."""
    t0 = time.perf_counter()
    open_heap = [(manhattan(start, goal), 0, start)]
    g_score = {start: 0}
    parent = {start: None}
    expanded = 0
    while open_heap:
        _, g, node = heapq.heappop(open_heap)
        if node == goal:
            return reconstruct(parent, start, goal), expanded, \
                time.perf_counter() - t0
        expanded += 1
        for nxt in neighbors(maze, node):
            tentative = g + 1
            if nxt not in g_score or tentative < g_score[nxt]:
                g_score[nxt] = tentative
                parent[nxt] = node
                f = tentative + manhattan(nxt, goal)
                heapq.heappush(open_heap, (f, tentative, nxt))
    return None, expanded, time.perf_counter() - t0


# ---------------------------------------------------------------------------
# Visualisation
# ---------------------------------------------------------------------------

def print_solution(maze, path):
    """Overlay the solution path on the maze and print it."""
    if path is None:
        print("No path found.")
        return
    grid = [row[:] for row in maze]
    for r, c in path:
        if grid[r][c] not in ("S", "G"):
            grid[r][c] = "*"
    for row in grid:
        print("  " + " ".join(row))


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

MAZE = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", ".", ".", "#", ".", ".", ".", ".", "#"],
    ["#", "#", "#", ".", "#", ".", "#", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", "#", ".", "#"],
    ["#", ".", "#", "#", "#", "#", ".", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", ".", "G"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
]


def main():
    start = find_cell(MAZE, "S")
    goal = find_cell(MAZE, "G")

    algorithms = [
        ("BFS", bfs_maze),
        ("DFS", dfs_maze),
        ("A*", astar_maze),
    ]

    for name, solver in algorithms:
        path, expanded, elapsed = solver(MAZE, start, goal)
        length = len(path) - 1 if path else "FAIL"
        print("\n=== %s ===" % name)
        print("Path length    : %s steps" % length)
        print("Nodes expanded : %d" % expanded)
        print("Time           : %.3f ms" % (elapsed * 1000))
        print_solution(MAZE, path)


if __name__ == "__main__":
    main()
