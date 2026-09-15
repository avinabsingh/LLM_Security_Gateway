import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
)

# ---------------------------------------
# Paths
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
TRAIN_PATH = BASE_DIR / "training" / "artifacts" / "hybrid_train_features.csv"
TEST_PATH = BASE_DIR / "training" / "artifacts" / "hybrid_test_features.csv"

MODEL_PATH = BASE_DIR / "models" / "hybrid" / "hybrid_rf_model.joblib"
SCALER_PATH = BASE_DIR / "models" / "hybrid" / "hybrid_rf_scaler.joblib"

# ---------------------------------------
# 1. Load Data
# ---------------------------------------
print("=" * 60)
print("TRAINING RANDOM FOREST HYBRID MODEL")
print("=" * 60)

train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

feature_columns = [col for col in train_df.columns if col not in ["prompt", "label"]]

X_train = train_df[feature_columns]
y_train = train_df["label"]

X_test = test_df[feature_columns]
y_test = test_df["label"]

# ---------------------------------------
# 2. Scale Data 
# (Not strictly required for RF, but keeps inference pipeline intact)
# ---------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------
# 3. Train Random Forest
# ---------------------------------------
print(f"Training on {len(X_train)} samples...")

rf_model = RandomForestClassifier(
    n_estimators=100,      # Number of trees in the forest
    max_depth=15,          # Maximum depth of each tree
    random_state=42,       # For reproducible results
    class_weight="balanced" # Helps if attacks are rare compared to safe prompts
)

rf_model.fit(X_train_scaled, y_train)
print("Training complete.")

# ---------------------------------------
# 4. Save Artifacts
# ---------------------------------------
# Ensure directory exists
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(rf_model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)
print(f"Saved model to: {MODEL_PATH.name}")

# ---------------------------------------
# 5. Evaluate on Test Set
# ---------------------------------------
predictions = rf_model.predict(X_test_scaled)

precision = precision_score(y_test, predictions, zero_division=0) * 100
recall = recall_score(y_test, predictions, zero_division=0) * 100
cm = confusion_matrix(y_test, predictions)

print("\n" + "=" * 60)
print("RANDOM FOREST RESULTS")
print("=" * 60)
print(f"Precision : {precision:.2f}%")
print(f"Recall    : {recall:.2f}%")
print("\n[CONFUSION MATRIX]")
print(f"TN = {cm[0][0]:<6} FP = {cm[0][1]}")
print(f"FN = {cm[1][0]:<6} TP = {cm[1][1]}")
print("=" * 60)