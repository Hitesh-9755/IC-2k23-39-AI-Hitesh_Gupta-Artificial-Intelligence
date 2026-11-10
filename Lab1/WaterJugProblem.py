"""
Water Jug Problem
================
Given two jugs of capacities jug1 and jug2 litres and an unlimited
water supply, measure exactly `target` litres using these operations:

    1. Fill a jug completely.
    2. Empty a jug completely.
    3. Pour water from one jug into another until the source is empty
       or the destination is full.

Solved using Breadth-First Search over states (jug1, jug2).
"""

from collections import deque


def get_successors(state, cap1, cap2):
    """Generate all states reachable from `state` in one move."""
    a, b = state
    successors = set()

    # Fill jug 1 / jug 2
    successors.add((cap1, b))
    successors.add((a, cap2))

    # Empty jug 1 / jug 2
    successors.add((0, b))
    successors.add((a, 0))

    # Pour jug 1 -> jug 2
    transfer = min(a, cap2 - b)
    successors.add((a - transfer, b + transfer))

    # Pour jug 2 -> jug 1
    transfer = min(b, cap1 - a)
    successors.add((a + transfer, b - transfer))

    successors.discard(state)
    return sorted(successors)


def water_jug_bfs(cap1, cap2, target):
    """Solve the water jug problem with BFS.

    Returns the list of states from start to goal, or None if there
    is no solution.
    """
    if target > max(cap1, cap2):
        return None

    start = (0, 0)
    queue = deque([start])
    parent = {start: None}

    while queue:
        state = queue.popleft()

        # Goal test: either jug has exactly `target` litres
        if state[0] == target or state[1] == target:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]

        for nxt in get_successors(state, cap1, cap2):
            if nxt not in parent:
                parent[nxt] = state
                queue.append(nxt)

    return None


def describe_path(path):
    """Print the solution path."""
    print("Solution path (jug1, jug2):")
    for i, state in enumerate(path):
        print("  Step %2d: (%2d, %2d) litres" % (i, state[0], state[1]))


def main():
    cases = [(4, 3, 2), (5, 3, 4)]
    for cap1, cap2, target in cases:
        print("Water Jug Problem: capacities = (%d, %d), target = %d litres\n"
              % (cap1, cap2, target))
        path = water_jug_bfs(cap1, cap2, target)
        if path is None:
            print("No solution exists for the given parameters.\n")
        else:
            describe_path(path)
            print("\nSolved in %d moves.\n" % (len(path) - 1))
        print("-" * 50)


if __name__ == "__main__":
    main()
