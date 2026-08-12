import os
import joblib
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    accuracy_score,
    confusion_matrix
)

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "evaluation",
    "fusion",
    "risk_fusion_test.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "risk_fusion",
    "risk_fusion_logistic_regression.joblib"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "risk_fusion",
    "risk_fusion_scaler.joblib"
)

print("=" * 80)
print("RISK FUSION THRESHOLD ANALYSIS")
print("=" * 80)

df = pd.read_csv(DATA_PATH)

FEATURE_COLUMNS = [
    c for c in df.columns
    if c not in ["prompt", "label"]
]

X = df[FEATURE_COLUMNS]
y = df["label"]

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

X_scaled = scaler.transform(X)

probabilities = model.predict_proba(X_scaled)[:, 1]

thresholds = [
    0.85,
    0.86,
    0.87,
    0.88,
    0.89,
    0.90,
    0.91,
    0.92,
    0.93,
    0.94,
    0.95,
    0.96,
    0.97,
    0.98,
    0.99
]

print("\nThreshold Analysis\n")

print(
    f"{'Threshold':<10}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1':<12}"
    f"{'Accuracy':<12}"
    f"{'FP':<10}"
    f"{'FN':<10}"
)

print("-" * 80)

results = []

for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y,
        predictions,
        zero_division=0
    )

    accuracy = accuracy_score(
        y,
        predictions
    )

    tn, fp, fn, tp = confusion_matrix(
        y,
        predictions
    ).ravel()

    results.append({
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
        "fp": fp,
        "fn": fn
    })

    print(
        f"{threshold:<10.2f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
        f"{accuracy:<12.4f}"
        f"{fp:<10}"
        f"{fn:<10}"
    )


# Best F1
best_f1 = max(
    results,
    key=lambda x: x["f1"]
)

# Best threshold with recall >= 95%
eligible = [
    r for r in results
    if r["recall"] >= 0.95
]

if eligible:

    best_high_recall = max(
        eligible,
        key=lambda x: x["precision"]
    )

    print("\n" + "=" * 80)
    print("BEST HIGH-RECALL THRESHOLD")
    print("=" * 80)

    print(best_high_recall)


print("\n" + "=" * 80)
print("BEST F1 THRESHOLD")
print("=" * 80)

print(best_f1)