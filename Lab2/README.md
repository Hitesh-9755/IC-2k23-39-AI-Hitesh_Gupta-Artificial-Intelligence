# Lab 2 — Heuristic Search Algorithms

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Implement uninformed (BFS, DFS) and informed (Hill Climbing, Best-First,
  A*) search algorithms.
- Apply them to maze navigation, the 8-puzzle, and route planning.
- Compare algorithms on execution time, nodes expanded, and solution quality.

## Files

| File | Description |
|------|-------------|
| `SearchAlgorithms.py` | BFS, DFS, Hill Climbing, Best-First, A* on a weighted graph |
| `MazeSolver.py` | BFS / DFS / A* on a 2-D grid maze |
| `EightPuzzleSolver.py` | BFS / A* on the 8-puzzle sliding-tile problem |
| `SearchAlgorithms.ipynb` | Notebook walkthrough with visualisations |

## Algorithm & Mathematical Foundation

### Search formulation
- **State space** `S`: all reachable configurations.
- **Initial state** `s0`, **goal test** `G(s)`, **operators** `Actions(s)`.
- **Path cost** `g(n)`: accumulated cost from `s0` to `n`.
- **Heuristic** `h(n)`: estimated cost from `n` to goal.

### Algorithms

| Algorithm | Evaluation | Complete | Optimal |
|-----------|-----------|----------|---------|
| BFS | depth | Yes (finite, unweighted) | Yes |
| DFS | depth | Yes | No |
| Hill Climbing | `h(n)` only | No | No |
| Best-First | `h(n)` only | No | No |
| A* | `f(n) = g(n) + h(n)` | Yes (admissible h) | Yes |

For the 8-puzzle, `h(n)` = Manhattan distance:

```
h(n) = Σ |row(tile) - row(goal)| + |col(tile) - col(goal)|
```

For the maze, `h(n)` = Manhattan distance to goal cell.

## Execution Instructions

```bash
cd Lab2
python SearchAlgorithms.py
python MazeSolver.py
python EightPuzzleSolver.py
jupyter notebook SearchAlgorithms.ipynb
```

## Results

### Route Planning (Arad → Bucharest)

| Algorithm | Path Length (edges) | Nodes Expanded | Time (ms) |
|-----------|--------------------|----------------|-----------|
| BFS | 9 | ~20 | <1 |
| DFS | 15+ | ~15 | <1 |
| Hill Climbing | FAIL (local min) | ~5 | <1 |
| Best-First | 12 | ~10 | <1 |
| A* | 9 | ~15 | <1 |

A* finds the optimal path while expanding fewer nodes than BFS.

### Maze Solver

| Algorithm | Path Length | Nodes Expanded | Time (ms) |
|-----------|------------|----------------|-----------|
| BFS | shortest | ~30 | <1 |
| DFS | longer | ~25 | <1 |
| A* | shortest | ~15 | <1 |

### 8-Puzzle

| Algorithm | Solution Length | Nodes Expanded | Time (ms) |
|-----------|----------------|----------------|-----------|
| BFS | optimal | ~50 000+ | ~500 |
| A* | optimal | ~500–2 000 | ~10 |

A* with Manhattan distance dramatically reduces the search space.

## Performance Analysis

- **BFS** explores all nodes at depth `d` before `d+1`; optimal for
  unweighted graphs but memory-heavy.
- **DFS** uses less memory but can get stuck in deep unproductive branches.
- **Hill Climbing** has no backtracking — fails on plateaus and local minima.
- **Best-First** ignores path cost; may return suboptimal paths.
- **A*** balances cost-so-far and heuristic estimate; with an admissible
  heuristic it is both complete and optimal.

## Learning Outcomes

- Formulate search problems with states, operators, and goal tests.
- Implement and compare uninformed vs. informed search strategies.
- Understand admissibility, completeness, and optimality trade-offs.
- Apply heuristics (Manhattan distance) to reduce search space.
