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
# Project Root
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

# ---------------------------------------
# Paths (Pointing to RF Models)
# ---------------------------------------
TEST_PATH = BASE_DIR / "training" / "artifacts" / "hybrid_test_features.csv"
MODEL_PATH = BASE_DIR / "models" / "hybrid" / "hybrid_rf_model.joblib"
SCALER_PATH = BASE_DIR / "models" / "hybrid" / "hybrid_rf_scaler.joblib"

# ---------------------------------------
# Load Test Data
# ---------------------------------------
print("=" * 80)
print("LOADING RANDOM FOREST TEST DATA")
print("=" * 80)

df = pd.read_csv(TEST_PATH)
print(f"Test samples: {len(df)}")

feature_columns = [col for col in df.columns if col not in ["prompt", "label"]]
X = df[feature_columns]
y = df["label"]

# ---------------------------------------
# Load Model & Scaler
# ---------------------------------------
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print("Random Forest Model loaded.")
print("Scaler loaded.")

# ---------------------------------------
# Scale & Predict
# ---------------------------------------
X_scaled = scaler.transform(X)

predictions = model.predict(X_scaled)
probabilities = model.predict_proba(X_scaled)[:, 1]

# ---------------------------------------
# Metrics
# ---------------------------------------
accuracy = accuracy_score(y, predictions)
precision = precision_score(y, predictions, zero_division=0)
recall = recall_score(y, predictions, zero_division=0)
f1 = f1_score(y, predictions, zero_division=0)
roc_auc = roc_auc_score(y, probabilities)

# ---------------------------------------
# Results
# ---------------------------------------
print("\n" + "=" * 80)
print("RANDOM FOREST RESULTS")
print("=" * 80)
print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC-AUC   : {roc_auc:.4f}")

print("\n" + "=" * 80)
print("CONFUSION MATRIX")
print("=" * 80)
cm = confusion_matrix(y, predictions)
print(cm)

print("\n" + "=" * 80)
print("CLASSIFICATION REPORT")
print("=" * 80)
print(
    classification_report(
        y,
        predictions,
        target_names=["Safe", "Attack"],
        zero_division=0
    )
)