"""
Missionaries and Cannibals Problem
===================================
Three missionaries and three cannibals must cross a river using a boat
that can carry at most two people.  At no point may the cannibals
outnumber the missionaries on either bank.

Solved with Breadth-First Search over states
(missionaries_left, cannibals_left, boat_side).
"""

from collections import deque

TOTAL = 3


def is_valid(state):
    """Check that cannibals never outnumber missionaries on a bank."""
    m_left, c_left, _ = state
    m_right = TOTAL - m_left
    c_right = TOTAL - c_left

    if m_left > 0 and c_left > m_left:
        return False
    if m_right > 0 and c_right > m_right:
        return False
    return True


def get_successors(state):
    """Generate all legal successor states."""
    m, c, side = state
    successors = []

    if side == 0:  # boat on left bank -> move people to right
        for dm in range(m + 1):
            for dc in range(c + 1):
                if 1 <= dm + dc <= 2:
                    nxt = (m - dm, c - dc, 1)
                    if is_valid(nxt):
                        successors.append(nxt)
    else:  # boat on right bank -> move people to left
        m_right = TOTAL - m
        c_right = TOTAL - c
        for dm in range(m_right + 1):
            for dc in range(c_right + 1):
                if 1 <= dm + dc <= 2:
                    nxt = (m + dm, c + dc, 0)
                    if is_valid(nxt):
                        successors.append(nxt)

    return successors


def solve_missionaries_cannibals():
    """Solve using BFS and return the path of states."""
    start = (TOTAL, TOTAL, 0)
    goal = (0, 0, 1)

    queue = deque([start])
    parent = {start: None}

    while queue:
        state = queue.popleft()
        if state == goal:
            path = []
            while state is not None:
                path.append(state)
                state = parent[state]
            return path[::-1]

        for nxt in get_successors(state):
            if nxt not in parent:
                parent[nxt] = state
                queue.append(nxt)

    return None


def describe_state(state):
    """Human-readable description of a state."""
    m, c, side = state
    boat = "LEFT " if side == 0 else "RIGHT"
    return ("Left bank: %dM %dC | Right bank: %dM %dC | Boat: %s"
            % (m, c, TOTAL - m, TOTAL - c, boat))


def main():
    print("Missionaries and Cannibals Problem (3M, 3C)\n")
    path = solve_missionaries_cannibals()
    if path is None:
        print("No solution exists.")
        return

    print("Solution found in %d crossings:\n" % (len(path) - 1))
    for i, state in enumerate(path):
        print("  Step %2d: %s" % (i, describe_state(state)))


if __name__ == "__main__":
    main()
