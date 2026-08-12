import pandas as pd
import joblib

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

TEST_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "test.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "baseline"
    / "logistic_regression.joblib"
)

VECTORIZER_PATH = (
    BASE_DIR
    / "models"
    / "baseline"
    / "tfidf_vectorizer.joblib"
)


# ---------------------------------------
# Load Test Data
# ---------------------------------------

print("=" * 60)
print("Loading Test Dataset")
print("=" * 60)

df = pd.read_csv(TEST_PATH)

X_text = df["prompt"].astype(str)
y_true = df["label"]

print(f"Test samples: {len(df)}")


# ---------------------------------------
# Load Model
# ---------------------------------------

print("\n" + "=" * 60)
print("Loading Model")
print("=" * 60)

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(VECTORIZER_PATH)

print("Model loaded.")
print("Vectorizer loaded.")


# ---------------------------------------
# Transform Test Data
# ---------------------------------------

print("\n" + "=" * 60)
print("Transforming Test Data")
print("=" * 60)

X_test = vectorizer.transform(X_text)

print(f"Test feature matrix: {X_test.shape}")


# ---------------------------------------
# Predictions
# ---------------------------------------

print("\n" + "=" * 60)
print("Generating Predictions")
print("=" * 60)

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]


# ---------------------------------------
# Metrics
# ---------------------------------------

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_true,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_true,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_true,
    y_probability
)


# ---------------------------------------
# Results
# ---------------------------------------

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")


# ---------------------------------------
# Confusion Matrix
# ---------------------------------------

cm = confusion_matrix(
    y_true,
    y_pred
)

print("\n" + "=" * 60)
print("CONFUSION MATRIX")
print("=" * 60)

print(cm)


# ---------------------------------------
# Classification Report
# ---------------------------------------

print("\n" + "=" * 60)
print("CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_true,
        y_pred,
        target_names=[
            "Safe",
            "Attack"
        ],
        zero_division=0
    )
)