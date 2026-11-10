"""
8-Puzzle Solver
===============
Solves the classic 8-puzzle sliding-tile problem using BFS and A*
with the Manhattan distance heuristic.

State: a tuple of 9 integers, e.g. (1, 2, 3, 4, 5, 6, 7, 8, 0)
where 0 is the blank tile.

Goal state: (1, 2, 3, 4, 5, 6, 7, 8, 0)
"""

import heapq
import time
from collections import deque

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def get_successors(state):
    """Generate all states reachable by sliding a tile into the blank."""
    blank = state.index(0)
    row, col = divmod(blank, 3)
    successors = []

    for offset in (-3, 3, -1, 1):
        nxt = blank + offset
        if nxt < 0 or nxt >= 9:
            continue
        # prevent horizontal wrap-around
        if offset in (-1, 1):
            new_col = col - 1 if offset == -1 else col + 1
            if divmod(nxt, 3)[1] != new_col:
                continue
        lst = list(state)
        lst[blank], lst[nxt] = lst[nxt], lst[blank]
        successors.append(tuple(lst))
    return successors


def manhattan_distance(state):
    """Sum of Manhattan distances of each tile from its goal position."""
    total = 0
    for i, tile in enumerate(state):
        if tile == 0:
            continue
        goal_pos = GOAL.index(tile)
        total += abs(i // 3 - goal_pos // 3) + abs(i % 3 - goal_pos % 3)
    return total


def reconstruct(parent, start, goal):
    """Rebuild the state path."""
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

def bfs_8puzzle(start, max_states=200000):
    """BFS solver - guarantees optimal solution but can be slow."""
    t0 = time.perf_counter()
    queue = deque([start])
    parent = {start: None}
    expanded = 0

    while queue and expanded < max_states:
        state = queue.popleft()
        expanded += 1
        if state == GOAL:
            path = reconstruct(parent, start, GOAL)
            return path, expanded, time.perf_counter() - t0
        for nxt in get_successors(state):
            if nxt not in parent:
                parent[nxt] = state
                queue.append(nxt)
    return None, expanded, time.perf_counter() - t0


def astar_8puzzle(start, max_states=200000):
    """A* solver with Manhattan distance heuristic."""
    t0 = time.perf_counter()
    open_heap = [(manhattan_distance(start), 0, start)]
    g_score = {start: 0}
    parent = {start: None}
    expanded = 0

    while open_heap and expanded < max_states:
        _, g, state = heapq.heappop(open_heap)
        if state == GOAL:
            path = reconstruct(parent, start, GOAL)
            return path, expanded, time.perf_counter() - t0
        expanded += 1
        for nxt in get_successors(state):
            tentative = g + 1
            if nxt not in g_score or tentative < g_score[nxt]:
                g_score[nxt] = tentative
                parent[nxt] = state
                f = tentative + manhattan_distance(nxt)
                heapq.heappush(open_heap, (f, tentative, nxt))
    return None, expanded, time.perf_counter() - t0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def print_state(state):
    """Pretty-print a 3x3 puzzle state."""
    for i in range(0, 9, 3):
        print("  " + " ".join(str(t) if t != 0 else "_"
                            for t in state[i:i + 3]))


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main():
    # A moderately difficult puzzle
    start = (2, 4, 3, 1, 5, 6, 7, 8, 0)

    print("Initial state:")
    print_state(start)
    print("\nGoal state:")
    print_state(GOAL)

    for name, solver in [("BFS", bfs_8puzzle), ("A*", astar_8puzzle)]:
        path, expanded, elapsed = solver(start)
        moves = len(path) - 1 if path else "FAIL"
        print("\n=== %s ===" % name)
        print("Solution length : %s moves" % moves)
        print("Nodes expanded  : %d" % expanded)
        print("Time            : %.1f ms" % (elapsed * 1000))
        if path:
            print("\nFirst few states:")
            for state in path[:4]:
                print_state(state)
                print()


if __name__ == "__main__":
    main()
