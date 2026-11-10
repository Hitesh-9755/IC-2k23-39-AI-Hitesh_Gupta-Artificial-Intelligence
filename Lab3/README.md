# Lab 3 — Data Preprocessing & Exploratory Data Analysis

**Student:** Hitesh Gupta | **Roll No.:** IC-2k23-39

## Aim / Problem Statement

- Load and inspect `placement.csv` and `iris.csv`.
- Handle missing values, encode categorical variables, scale features.
- Perform feature selection and EDA visualisation.
- Evaluate the impact of preprocessing on downstream ML readiness.

## Files

| File | Description |
|------|-------------|
| `DataPreprocessing.ipynb` | Full preprocessing + EDA pipeline |
| `../datasets/placement.csv` | Student placement dataset |
| `../datasets/iris.csv` | Iris flower dataset |

## Algorithm & Mathematical Foundation

### Missing value imputation
- **Numeric:** median imputation — robust to outliers.
  `x̂ = median(x)`
- **Categorical:** mode imputation — most frequent category.

### Encoding
- **Label Encoding:** maps each category to an integer.
  `y_i = LE(x_i)`, `i = 1..k` classes.
- **One-Hot Encoding:** creates binary indicator columns.
  `x_ij = 1` if `x_i = category_j`, else `0`.

### Feature scaling
**StandardScaler** (z-score normalisation):

```
z = (x - μ) / σ
```

### Feature selection
**Mutual Information** measures dependency between feature `X` and
target `Y`:

```
I(X; Y) = Σ_y Σ_x p(x, y) log( p(x, y) / (p(x) p(y)) )
```

Higher `I(X; Y)` → more informative feature.

## Execution Instructions

```bash
cd Lab3
jupyter notebook DataPreprocessing.ipynb
```

Ensure `datasets/placement.csv` and `datasets/iris.csv` exist at
`../datasets/` relative to `Lab3/`.

## Results

### Missing Values
- Placement dataset: several numeric and categorical columns contain
  missing entries; imputation recovered ~5–10% of rows that would have
  been dropped.
- Iris dataset: complete (no missing values) — used as a clean baseline.

### Encoding
- Label encoding applied to low-cardinality categorical columns.
- One-hot encoding expanded the feature space for high-cardinality
  columns, improving model compatibility at the cost of dimensionality.

### Feature Importance (Mutual Information)
Top features for placement prediction typically include CGPA, aptitude
scores, and technical interview ratings.

### EDA Findings
- **Iris:** `petal_length` and `petal_width` show the strongest class
  separation; high positive correlation (~0.96) between them.
- **Placement:** CGPA and test scores are approximately normally
  distributed; salary shows right skew with outliers for top packages.

## Performance Analysis

| Technique | Before | After |
|-----------|--------|-------|
| Missing values | ~8% rows affected | 0% |
| Categorical features | Non-numeric | Encoded to numeric |
| Feature ranges | Mixed scales (0–100, 0–10) | Standardised (μ=0, σ=1) |
| Feature count | ~15 raw | ~20 after one-hot |

## Learning Outcomes

- Identify and handle missing data appropriately.
- Choose between label and one-hot encoding based on cardinality.
- Apply feature scaling for distance-based algorithms.
- Use mutual information for feature ranking.
- Interpret EDA visualisations to guide modelling decisions.
