# Lab 5 — Machine Learning for Intelligent Decision Making

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Implement a Decision Tree Classifier using Scikit-Learn.
- Apply it to the Iris dataset (and optionally placement data).
- Generate confusion matrix, classification report, and tree visualisations.
- Evaluate hyperparameter tuning (`max_depth`, `criterion`).

## Files

| File | Description |
|------|-------------|
| `DecisionTree.ipynb` | Full ML pipeline: train, evaluate, tune, save |
| `../datasets/iris.csv` | Iris classification dataset |
| `../models/decision_tree.pkl` | Trained model artifact |

## Algorithm & Mathematical Foundation

### Decision Tree Learning
A decision tree recursively partitions the feature space using
axis-aligned splits. At each node, the best split is chosen by
maximising information gain (or minimising impurity).

**Gini Impurity:**

```
Gini(D) = 1 - Σ p_k²
```

**Entropy (Information Gain):**

```
H(D) = -Σ p_k log₂(p_k)
IG(D, A) = H(D) - Σ_v (|D_v| / |D|) H(D_v)
```

The tree stops splitting when `max_depth` is reached, all samples belong
to one class, or `min_samples_split` is not met.

### Evaluation Metrics

```
Accuracy  = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 · Precision · Recall / (Precision + Recall)
```

## Execution Instructions

```bash
cd Lab5
jupyter notebook DecisionTree.ipynb
```

## Results

### Default Model (Iris)

| Metric | Value |
|--------|-------|
| Accuracy | ~0.98 |
| Precision (weighted) | ~0.98 |
| Recall (weighted) | ~0.98 |
| F1-score (weighted) | ~0.98 |

### Confusion Matrix
Near-diagonal matrix — only 1–2 misclassifications out of 45 test samples.

### Hyperparameter Tuning

| criterion | max_depth | CV Accuracy |
|-----------|-----------|-------------|
| gini | None | ~0.96 |
| gini | 3 | ~0.95 |
| gini | 5 | ~0.97 |
| entropy | None | ~0.96 |
| entropy | 5 | ~0.97 |

Shallow trees (depth 3–5) achieve comparable accuracy with better
generalisation and interpretability.

## Performance Analysis

- **Strengths:** Interpretable, handles non-linear boundaries, no feature
  scaling required.
- **Weaknesses:** High variance (overfitting), unstable to small data
  changes.
- **Tuning insight:** `max_depth` is the most impactful parameter;
  `criterion` (gini vs. entropy) has minimal effect on Iris.

## Learning Outcomes

- Train and evaluate a Decision Tree classifier.
- Interpret confusion matrices and classification reports.
- Visualise decision boundaries and tree structure.
- Perform hyperparameter tuning with cross-validation.
- Save trained models for reuse.
