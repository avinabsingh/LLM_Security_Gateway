import pandas as pd
import joblib

from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


# ---------------------------------------
# Project Root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


# ---------------------------------------
# Paths
# ---------------------------------------

TRAIN_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "hybrid_train_features.csv"
)

MODEL_DIR = (
    BASE_DIR
    / "models"
    / "hybrid"
)

MODEL_PATH = (
    MODEL_DIR
    / "hybrid_logistic_regression.joblib"
)

SCALER_PATH = (
    MODEL_DIR
    / "hybrid_scaler.joblib"
)


# ---------------------------------------
# Create Model Directory
# ---------------------------------------

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# Load Data
# ---------------------------------------

print("=" * 80)
print("LOADING HYBRID TRAINING DATA")
print("=" * 80)

df = pd.read_csv(
    TRAIN_PATH
)

print(
    f"Training samples: {len(df)}"
)


# ---------------------------------------
# Feature Columns
# ---------------------------------------

feature_columns = [
    column
    for column in df.columns
    if column not in [
        "prompt",
        "label"
    ]
]


X = df[
    feature_columns
]

y = df[
    "label"
]


print(
    f"Feature matrix: {X.shape}"
)


print("\nLabel Distribution:")

print(
    y.value_counts()
)


# ---------------------------------------
# Scale Features
# ---------------------------------------

print("\n" + "=" * 80)
print("SCALING FEATURES")
print("=" * 80)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    X
)


print(
    f"Scaled matrix: {X_scaled.shape}"
)


# ---------------------------------------
# Train Model
# ---------------------------------------

print("\n" + "=" * 80)
print("TRAINING HYBRID MODEL")
print("=" * 80)

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(
    X_scaled,
    y
)


print(
    "Hybrid model training completed."
)


# ---------------------------------------
# Save Model
# ---------------------------------------

joblib.dump(
    model,
    MODEL_PATH
)

joblib.dump(
    scaler,
    SCALER_PATH
)


# ---------------------------------------
# Final Report
# ---------------------------------------

print("\n" + "=" * 80)
print("MODEL SAVED")
print("=" * 80)

print(
    f"Model  : {MODEL_PATH}"
)

print(
    f"Scaler : {SCALER_PATH}"
)