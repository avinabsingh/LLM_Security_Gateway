import os
import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
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
print("LOADING RISK FUSION TEST DATA")
print("=" * 80)

df = pd.read_csv(DATA_PATH)

print(f"Test samples: {len(df)}")
print(f"Dataset shape: {df.shape}")

TARGET = "label"

FEATURE_COLUMNS = [
    c for c in df.columns
    if c not in ["prompt", TARGET]
]

X = df[FEATURE_COLUMNS]
y = df[TARGET]

print(f"Feature matrix: {X.shape}")

print("\nLabel Distribution:")
print(y.value_counts())


print("\nLoading Risk Fusion model...")
model = joblib.load(MODEL_PATH)

print("Model loaded.")

print("Loading scaler...")
scaler = joblib.load(SCALER_PATH)

print("Scaler loaded.")


X_scaled = scaler.transform(X)

print(f"Scaled matrix: {X_scaled.shape}")


# Attack probability

y_prob = model.predict_proba(X_scaled)[:, 1]

# Final Risk Fusion threshold

THRESHOLD = 0.92

# Predictions using selected threshold

y_pred = (y_prob >= THRESHOLD).astype(int)


# Metrics
accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, zero_division=0)
recall = recall_score(y, y_pred, zero_division=0)
f1 = f1_score(y, y_pred, zero_division=0)
roc_auc = roc_auc_score(y, y_prob)

cm = confusion_matrix(y, y_pred)


print("\n" + "=" * 80)
print("RISK FUSION TEST PERFORMANCE")
print("=" * 80)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")


print("\nConfusion Matrix:")
print(cm)


print("\nClassification Report:")
print(
    classification_report(
        y,
        y_pred,
        target_names=["Safe", "Attack"],
        zero_division=0
    )
)


print("\n" + "=" * 80)
print("CONFUSION MATRIX DETAILS")
print("=" * 80)

tn, fp, fn, tp = cm.ravel()

print(f"True Negatives  : {tn}")
print(f"False Positives : {fp}")
print(f"False Negatives : {fn}")
print(f"True Positives  : {tp}")


print("\nAttack Detection Rate:")
print(f"{tp / (tp + fn):.4f}")

print("\nSafe Flag Rate:")
print(f"{fp / (fp + tn):.4f}")