"""
Mini Project — Explainable AI Dashboard
=======================================
A lightweight Streamlit-free dashboard that combines:
    1. A trained Decision Tree classifier (Iris).
    2. Feature-importance visualisation.
    3. LIME-style local explanations (simplified).
    4. Interactive prediction from user input.

Run:
    python MiniProject/xai_dashboard.py
"""

from __future__ import annotations

import os
import pickle
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
                         "datasets", "iris.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..",
                          "models", "decision_tree.pkl")
OUT_DIR = os.path.join(os.path.dirname(__file__), "outputs")
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Data & Model
# ---------------------------------------------------------------------------

def load_data() -> tuple:
    """Load Iris dataset and return features, labels, feature names."""
    df = pd.read_csv(DATA_PATH)
    feature_cols = list(df.columns[:-1])
    X = df[feature_cols].values
    y = df.iloc[:, -1].values
    return X, y, feature_cols


def train_model(X: np.ndarray, y: np.ndarray) -> DecisionTreeClassifier:
    """Train a decision tree and return the fitted model."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y)
    clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Model accuracy on test set: {acc:.4f}")
    return clf


def save_model(clf: DecisionTreeClassifier) -> None:
    """Persist the trained model."""
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
    print(f"Model saved to {MODEL_PATH}")


def load_model() -> DecisionTreeClassifier:
    """Load a previously saved model, or train a new one."""
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    X, y, _ = load_data()
    return train_model(X, y)


# ---------------------------------------------------------------------------
# Explanations
# ---------------------------------------------------------------------------

def feature_importance(clf: DecisionTreeClassifier,
                       feature_names: List[str]) -> pd.DataFrame:
    """Return feature importances as a sorted DataFrame."""
    imp = clf.feature_importances_
    df = pd.DataFrame({"Feature": feature_names, "Importance": imp})
    return df.sort_values("Importance", ascending=False)


def plot_feature_importance(clf: DecisionTreeClassifier,
                            feature_names: List[str]) -> None:
    """Bar chart of feature importances."""
    df = feature_importance(clf, feature_names)
    plt.figure(figsize=(8, 4))
    plt.barh(df["Feature"], df["Importance"], color="steelblue")
    plt.xlabel("Importance")
    plt.title("Feature Importance — Decision Tree (Iris)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "feature_importance.png"),
                dpi=300, bbox_inches="tight")
    plt.show()


def plot_tree_visual(clf: DecisionTreeClassifier,
                     feature_names: List[str],
                     class_names: List[str]) -> None:
    """Visualise the decision tree structure."""
    plt.figure(figsize=(20, 10))
    plot_tree(clf, feature_names=feature_names,
              class_names=class_names, filled=True, rounded=True,
              fontsize=10)
    plt.title("Decision Tree — Iris Classification")
    plt.savefig(os.path.join(OUT_DIR, "decision_tree.png"),
                dpi=300, bbox_inches="tight")
    plt.show()


def explain_prediction(clf: DecisionTreeClassifier,
                       feature_names: List[str],
                       sample: np.ndarray,
                       class_names: List[str]) -> str:
    """Return a human-readable explanation of a single prediction."""
    pred = clf.predict(sample.reshape(1, -1))[0]
    proba = clf.predict_proba(sample.reshape(1, -1))[0]
    tree_text = export_text(clf, feature_names=feature_names,
                            max_depth=4)
    lines = [
        f"Predicted class : {pred}",
        f"Class probabilities: {dict(zip(class_names, proba.round(3)))}",
        "",
        "Decision path (simplified):",
    ]
    # Extract the path by walking the tree
    node = 0
    while clf.tree_.feature[node] != -2:  # not a leaf
        feat_idx = clf.tree_.feature[node]
        thresh = clf.tree_.threshold[node]
        feat_name = feature_names[feat_idx]
        val = sample[feat_idx]
        if val <= thresh:
            lines.append(f"  {feat_name} <= {thresh:.3f}  (value={val:.3f}) -> left")
            node = clf.tree_.children_left[node]
        else:
            lines.append(f"  {feat_name} >  {thresh:.3f}  (value={val:.3f}) -> right")
            node = clf.tree_.children_right[node]
    lines.append(f"  Leaf -> {class_names[pred]}")
    return "\n".join(lines)


def interactive_predict(clf: DecisionTreeClassifier,
                        feature_names: List[str],
                        class_names: List[str]) -> None:
    """Prompt user for feature values and explain the prediction."""
    print("\n=== Interactive Prediction ===")
    print("Enter feature values (or 'q' to quit):")
    while True:
        try:
            values = input(
                "  sepal_length, sepal_width, petal_length, petal_width: "
            )
            if values.strip().lower() == "q":
                break
            sample = np.array([float(v) for v in values.split(",")])
            print(explain_prediction(clf, feature_names, sample, class_names))
            print()
        except (ValueError, KeyboardInterrupt):
            print("Invalid input. Enter 4 comma-separated numbers.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("XAI DASHBOARD — Iris Decision Tree")
    print("=" * 60)

    X, y, feature_names = load_data()
    class_names = sorted(set(y))

    clf = load_model()
    if not os.path.exists(MODEL_PATH):
        save_model(clf)

    # 1. Feature importance
    print("\n--- Feature Importance ---")
    imp_df = feature_importance(clf, feature_names)
    print(imp_df.to_string(index=False))
    plot_feature_importance(clf, feature_names)

    # 2. Tree visualisation
    print("\n--- Decision Tree ---")
    plot_tree_visual(clf, feature_names, class_names)

    # 3. Sample explanation
    print("\n--- Sample Prediction Explanation ---")
    sample = X[0]
    print(explain_prediction(clf, feature_names, sample, class_names))

    # 4. Interactive mode
    interactive_predict(clf, feature_names, class_names)


if __name__ == "__main__":
    main()
