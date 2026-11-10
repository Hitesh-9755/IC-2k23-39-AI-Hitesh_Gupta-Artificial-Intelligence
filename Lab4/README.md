# Lab 4 — Knowledge Representation & Logical Reasoning

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Implement knowledge representation using predicates, semantic networks,
  frames, and a logical rule engine.
- Build a University Knowledge Base and a Medical Expert System KB.
- Compare Frames vs. Semantic Networks vs. Rule-Based Systems.

## Files

| File | Description |
|------|-------------|
| `SemanticNetworks.py` | Graph-based KR with IS-A inheritance reasoning |
| `RuleEngine.py` | Forward-chaining predicate logic engine |
| `KnowledgeRepresentation.ipynb` | Notebook combining all four techniques |

## Algorithm & Mathematical Foundation

### Semantic Networks
A semantic network is a directed labelled graph `G = (V, E)` where:
- `V` = concepts (nodes)
- `E ⊆ V × R × V` = labelled relationships (edges)

**Inheritance reasoning** uses transitive closure over IS-A edges:

```
is_a(x, y) ⟺ ∃ path x →IS-A→ ... →IS-A→ y
```

### Frames
A frame is a record structure:

```
Frame = ⟨name, slots⟩
slot  = ⟨slot_name, value, default, constraint⟩
```

Frames support inheritance via `AKO` (A-Kind-Of) links and procedural
attachments (methods on slots).

### Rule Engine (Forward Chaining)
Given facts `F` and rules `R = {(P_i → C_i)}`:

```
repeat
    for each rule r in R:
        if premises(r) ⊆ F and conclusion(r) ∉ F:
            F ← F ∪ {conclusion(r)}
until no new facts are added
```

This is a monotonic fixpoint computation; it terminates when
`F` reaches a fixed point.

## Execution Instructions

```bash
cd Lab4
python SemanticNetworks.py
python RuleEngine.py
jupyter notebook KnowledgeRepresentation.ipynb
```

## Results

### Semantic Network (University KB)
- 15+ nodes representing Person → Student/Faculty → Professor/Lecturer.
- Transitive IS-A queries correctly resolve `Alice → Student → Person`.
- Property retrieval returns course credits, department, instructor.

### Rule Engine (Medical KB)
```
FIRED: symptom(fever) AND symptom(cough) → condition(respiratory)
FIRED: symptom(fever) AND symptom(body_aches) → condition(flu_like)
FIRED: condition(respiratory) AND condition(flu_like) → diagnosis(influenza)
```

### Rule Engine (University KB)
Derives eligibility, honors status, and enrollment facts from student,
course, and grade predicates.

## Performance Analysis

| Technique | Nodes/Rules | Inference Steps | Query Time |
|-----------|------------|-----------------|------------|
| Semantic Network | ~20 nodes | O(V+E) traversal | <1 ms |
| Frames | ~5 frames | O(1) slot lookup | <1 ms |
| Rule Engine | ~10 rules | ~5 iterations | <1 ms |

## Frames vs. Semantic Networks vs. Rule-Based Systems

| Aspect | Frames | Semantic Networks | Rule-Based |
|--------|--------|-------------------|------------|
| **Structure** | Slot-value records | Graph (nodes+edges) | Facts + IF-THEN rules |
| **Inheritance** | Frame hierarchy (AKO) | IS-A link traversal | Rule chaining |
| **Reasoning** | Property inheritance, defaults | Graph search, transitive closure | Forward/backward chaining |
| **Strengths** | Compact object description | Visual concept hierarchies | Explainable decision logic |
| **Weaknesses** | Rigid structure | Complex for procedural knowledge | Rule explosion risk |
| **Best for** | Object-oriented domains | Taxonomies, ontologies | Expert systems, diagnostics |

## Learning Outcomes

- Represent knowledge using multiple formalisms.
- Implement transitive inheritance over semantic networks.
- Build forward-chaining inference engines over predicate logic.
- Compare KR techniques for different problem domains.
