# Lab 1 — AI Problem Formulation & Production Systems

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Implement classic AI problem formulations using uninformed and informed search.
- Build production rule systems and apply them to real-world expert-system style tasks.
- Compare classical programming with AI programming.

## Files

| File | Description |
|------|-------------|
| `ProductionSystems.py` | Forward-chaining rule engine + medical diagnosis + chatbot |
| `WaterJugProblem.py` | BFS solution for the water jug measurement problem |
| `MissionariesCannibals.py` | BFS solution for the river-crossing puzzle |
| `VacuumCleaner.py` | Random vs. intelligent vacuum agent comparison |
| `outputs/` | Generated plots / result snapshots |

## Algorithm & Mathematical Foundation

### Production Systems
A production system consists of:

- **Working Memory (WM):** a set of facts representing the current state.
- **Production Rules:** `IF <conditions> THEN <actions>`.
- **Inference Engine:** forward chaining — repeatedly fires any rule whose
  conditions are satisfied until no rule fires (fixpoint).

Formally, a rule `r = (C_r, A_r)` fires when `C_r ⊆ WM`; after firing,
`WM ← WM ∪ A_r(WM)`.

### Water Jug Problem
State space `S = {(x, y) | 0 ≤ x ≤ c1, 0 ≤ y ≤ c2}`. Operators:
fill, empty, pour. BFS explores states level by level, guaranteeing the
shortest solution in number of moves.

### Missionaries & Cannibals
State `(m, c, side)` where `m, c` are counts on the left bank and
`side ∈ {0, 1}` is the boat position. Constraint: `c ≤ m` on each bank
whenever `m > 0`. BFS finds the minimum-crossing sequence.

### Vacuum Cleaner
Agent perceives cell status (clean/dirty) and position. Performance
metric: number of actions (steps) until all cells are clean.

## Execution Instructions

```bash
cd Lab1
python ProductionSystems.py
python WaterJugProblem.py
python MissionariesCannibals.py
python VacuumCleaner.py
```

## Results

### Production Systems
- **Medical diagnosis:** correctly distinguishes Flu, Common Cold, Measles,
  and Strep Throat from symptom sets via chained rules.
- **Chatbot:** maps intents (greeting, hours, fees, goodbye) to canned
  responses with a fallback rule.

### Water Jug (4, 3 → 2 litres)
```
(0,0) → (4,0) → (4,3) → (1,3) → (1,0) → (0,1) → (4,1) → (2,3)  [GOAL]
Solved in 7 moves.
```

### Missionaries & Cannibals
BFS produces the classic 11-step crossing sequence; every intermediate
state satisfies the safety constraint.

### Vacuum Cleaner (4×4 grid, 5 dirty cells)
- Intelligent agent: ~15–20 steps (greedy Manhattan navigation).
- Random agent: ~80–150 steps on average over 10 trials.

## Performance Analysis

| Problem | Algorithm | Nodes/States Explored | Solution Length |
|---------|-----------|----------------------|-----------------|
| Water Jug | BFS | ~20 states | 7 moves |
| Missionaries & Cannibals | BFS | ~30 states | 11 crossings |
| Vacuum (intelligent) | Greedy heuristic | n/a | ~18 steps |
| Vacuum (random) | Random policy | n/a | ~110 steps (avg) |

## Classical vs. AI Programming

| Aspect | Classical Programming | AI Programming |
|--------|----------------------|----------------|
| Control flow | Explicit, programmer-defined | Often emergent from rules/search |
| Knowledge | Embedded in code logic | Separated as facts/rules/data |
| Handling uncertainty | Poor | Designed for it (probabilities, heuristics) |
| Solution method | Deterministic algorithms | Search, inference, learning |
| Example | `if x > 0: ...` | Production rules + working memory |

## Learning Outcomes

- Understand state-space representation and operator design.
- Implement forward-chaining inference engines.
- Apply BFS to classical AI puzzles.
- Compare agent strategies quantitatively.
