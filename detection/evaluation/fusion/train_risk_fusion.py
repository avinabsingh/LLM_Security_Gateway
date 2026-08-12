import os
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "evaluation",
    "fusion",
    "risk_fusion_train.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models",
    "risk_fusion"
)

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "risk_fusion_logistic_regression.joblib"
)

SCALER_PATH = os.path.join(
    MODEL_DIR,
    "risk_fusion_scaler.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 80)
print("LOADING RISK FUSION TRAINING DATA")
print("=" * 80)

df = pd.read_csv(DATA_PATH)

print(f"Training samples: {len(df)}")
print(f"Dataset shape   : {df.shape}")


# ============================================================
# FEATURES
# ============================================================

DROP_COLUMNS = [
    "prompt",
    "label"
]

X = df.drop(columns=DROP_COLUMNS)
y = df["label"]

print(f"Feature matrix: {X.shape}")

print("\nLabel Distribution:")
print(y.value_counts())


# ============================================================
# SCALE FEATURES
# ============================================================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print(f"\nScaled matrix: {X_scaled.shape}")


# ============================================================
# TRAIN MODEL
# ============================================================

print("\nTraining Risk Fusion Logistic Regression...")

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_scaled, y)

print("Risk Fusion model training completed.")


# ============================================================
# TRAINING PERFORMANCE
# ============================================================

train_predictions = model.predict(X_scaled)
train_probabilities = model.predict_proba(X_scaled)[:, 1]

print("\nTRAINING PERFORMANCE")

print(
    classification_report(
        y,
        train_predictions,
        target_names=["Safe", "Attack"]
    )
)

print(
    f"ROC-AUC: {roc_auc_score(y, train_probabilities):.4f}"
)


# ============================================================
# SAVE MODEL + SCALER
# ============================================================

joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("\nSaved model:")
print(MODEL_PATH)

print("\nSaved scaler:")
print(SCALER_PATH)