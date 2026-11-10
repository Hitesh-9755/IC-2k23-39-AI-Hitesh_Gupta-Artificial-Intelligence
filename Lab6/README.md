# Lab 6 — Deep Learning Fundamentals using PyTorch

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Implement tensor operations and automatic differentiation (autograd).
- Build a Linear Regression model with a PyTorch training loop.
- Compare loss functions (MSE) and optimisers (SGD vs. Adam).
- Apply to house price / student score prediction.

## Files

| File | Description |
|------|-------------|
| `PyTorchBasics.ipynb` | Tensors, autograd, loss functions, optimisers |
| `LinearRegressionPyTorch.ipynb` | Full training loop for linear regression |
| `../models/linear_regression.pt` | Saved model weights |

## Algorithm & Mathematical Foundation

### Linear Regression
Model: `ŷ = wx + b`

**Loss (MSE):**

```
L = (1/n) Σ (y_i - ŷ_i)²
```

**Gradient descent update:**

```
w ← w - η · ∂L/∂w
b ← b - η · ∂L/∂b
```

where `η` is the learning rate.

### Autograd
PyTorch builds a dynamic computation graph during the forward pass.
`loss.backward()` computes gradients via reverse-mode automatic
differentiation; `optimizer.step()` updates parameters.

### Optimisers
- **SGD:** `θ ← θ - η ∇L(θ)` — simple, may oscillate.
- **Adam:** adaptive learning rates per parameter using momentum and
  second-moment estimates — faster convergence.

## Execution Instructions

```bash
cd Lab6
jupyter notebook PyTorchBasics.ipynb
jupyter notebook LinearRegressionPyTorch.ipynb
```

## Results

### PyTorch Basics
- Tensor creation, reshaping, element-wise ops, reductions verified.
- Autograd correctly computes `dy/dx` for polynomial functions.
- Gradient descent on `(x-3)²` converges to `x ≈ 3` in ~30 iterations.

### Linear Regression
| Optimiser | Final MSE | Learned w | Learned b | True w | True b |
|-----------|-----------|-----------|-----------|--------|--------|
| SGD | ~2.0 | ~2.4 | ~1.1 | 2.5 | 1.0 |
| Adam | ~1.8 | ~2.5 | ~1.0 | 2.5 | 1.0 |

Adam converges faster and reaches lower loss.

## Performance Analysis

| Aspect | Traditional ML (Sklearn) | Deep Learning (PyTorch) |
|--------|--------------------------|-------------------------|
| Implementation | `LinearRegression().fit(X, y)` | Custom training loop |
| Flexibility | Fixed algorithm | Any architecture/loss |
| Gradient control | Automatic | Manual via autograd |
| GPU support | Limited | Full CUDA support |
| Interpretability | High (coefficients) | Moderate |

**Gradient convergence:** Loss decreases monotonically; Adam shows
smoother convergence due to adaptive learning rates.

## Learning Outcomes

- Manipulate PyTorch tensors and computation graphs.
- Implement custom training loops with autograd.
- Compare SGD and Adam optimisers empirically.
- Save and reload trained models.
- Understand when deep learning frameworks add value over classical ML.
