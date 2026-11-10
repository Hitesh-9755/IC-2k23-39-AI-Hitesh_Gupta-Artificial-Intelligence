# Lab 7 — Explainable AI, Adversarial AI & Advanced Applications

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Implement Grad-CAM visualisation on a pre-trained ResNet CNN.
- Evaluate Fast Gradient Sign Method (FGSM) adversarial attacks.
- Compare PCA vs. SVD for dimensionality reduction.
- Mini Project: Explainable AI Dashboard for Iris classification.

## Files

| File | Description |
|------|-------------|
| `GradCAM_XAI.ipynb` | Grad-CAM heatmaps on ResNet-18 |
| `FGSM_Adversarial.ipynb` | FGSM attack + robustness evaluation |
| `PCA_SVD_DimensionalityReduction.ipynb` | PCA vs SVD comparison |
| `MiniProject/xai_dashboard.py` | Interactive XAI dashboard |
| `MiniProject/outputs/` | Generated plots |

## Algorithm & Mathematical Foundation

### Grad-CAM
For target class `c` and conv layer activations `A^k`:

```
α_k^c = (1/Z) Σ_i Σ_j ∂y^c / ∂A^k_ij        (global avg pool of gradients)
L^c   = ReLU( Σ_k α_k^c · A^k )             (weighted combination)
```

The ReLU ensures only features with positive influence on class `c`
are highlighted.

### FGSM
```
x_adv = x + ε · sign(∇_x J(θ, x, y))
```

where `J` is the cross-entropy loss, `ε` controls perturbation size.
The attack is **white-box** (requires model gradients).

### PCA
Eigen-decomposition of the covariance matrix:

```
Σ = (1/n) X^T X = V Λ V^T
```

Top-`k` eigenvectors (principal components) capture maximum variance.

### SVD
Direct matrix factorisation:

```
X = U Σ V^T
```

PCA scores = `U_k Σ_k` (equivalent to projecting onto top right
singular vectors).

## Execution Instructions

```bash
cd Lab7
jupyter notebook GradCAM_XAI.ipynb
jupyter notebook FGSM_Adversarial.ipynb
jupyter notebook PCA_SVD_DimensionalityReduction.ipynb
python MiniProject/xai_dashboard.py
```

## Results

### Grad-CAM
- Heatmaps highlight object-discriminative regions (e.g., face for
  "golden retriever", wheels for "sports car").
- Last conv layer (`layer4[-1]`) gives best spatial resolution.

### FGSM
| Epsilon | Accuracy |
|---------|----------|
| 0.00 | ~75% |
| 0.01 | ~60% |
| 0.03 | ~40% |
| 0.05 | ~25% |
| 0.10 | ~10% |
| 0.20 | ~5% |

Even `ε=0.03` causes significant accuracy drop — model is vulnerable.

### PCA vs SVD
- Both produce identical 2-D projections (up to sign/rotation).
- Iris: 2 components capture ~98% variance.
- Classification accuracy after reduction: ~95% (vs ~97% full).

### Mini Project — XAI Dashboard
- Feature importance bar chart.
- Decision tree visualisation.
- Per-sample explanation with decision path.
- Interactive prediction mode.

## Performance Analysis

| Technique | Metric | Result |
|-----------|--------|--------|
| Grad-CAM | Spatial localisation | Correct object regions highlighted |
| FGSM | Accuracy drop at ε=0.05 | ~50% relative decrease |
| PCA | Variance retained (2 PCs) | ~98% |
| SVD | Equivalent to PCA | Identical projection |
| XAI Dashboard | Explanation latency | <10 ms per prediction |

## Learning Outcomes

- Explain CNN predictions using gradient-based attribution.
- Craft and evaluate adversarial examples.
- Apply PCA/SVD for dimensionality reduction.
- Build an interpretable ML dashboard.
- Understand model robustness and explainability trade-offs.
