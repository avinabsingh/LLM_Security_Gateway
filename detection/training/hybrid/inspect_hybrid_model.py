import pandas as pd
import joblib

from pathlib import Path


# ---------------------------------------
# Project Root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


MODEL_PATH = (
    BASE_DIR
    / "models"
    / "hybrid"
    / "hybrid_logistic_regression.joblib"
)

FEATURE_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "hybrid_train_features.csv"
)


# ---------------------------------------
# Load
# ---------------------------------------

print("=" * 80)
print("LOADING HYBRID MODEL")
print("=" * 80)

model = joblib.load(
    MODEL_PATH
)

df = pd.read_csv(
    FEATURE_PATH,
    nrows=1
)


feature_columns = [
    column
    for column in df.columns
    if column not in [
        "prompt",
        "label"
    ]
]


# ---------------------------------------
# Coefficients
# ---------------------------------------

coefficients = model.coef_[0]


importance = pd.DataFrame({

    "feature": feature_columns,

    "coefficient": coefficients,

    "absolute_importance": abs(
        coefficients
    )

})


importance = importance.sort_values(
    "absolute_importance",
    ascending=False
)


# ---------------------------------------
# Display
# ---------------------------------------

print("\n" + "=" * 80)
print("FEATURE IMPORTANCE")
print("=" * 80)

print(
    importance.to_string(
        index=False
    )
)


# ---------------------------------------
# Positive / Negative
# ---------------------------------------

print("\n" + "=" * 80)
print("TOP ATTACK-PUSHING FEATURES")
print("=" * 80)

print(
    importance[
        importance["coefficient"] > 0
    ].head(10).to_string(
        index=False
    )
)


print("\n" + "=" * 80)
print("TOP SAFE-PUSHING FEATURES")
print("=" * 80)

print(
    importance[
        importance["coefficient"] < 0
    ].head(10).to_string(
        index=False
    )
)