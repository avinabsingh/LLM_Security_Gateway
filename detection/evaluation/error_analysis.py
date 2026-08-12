import pandas as pd
import joblib

from pathlib import Path


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
# Load
# ---------------------------------------

df = pd.read_csv(TEST_PATH)

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(VECTORIZER_PATH)


# ---------------------------------------
# Predict
# ---------------------------------------

X = vectorizer.transform(
    df["prompt"].astype(str)
)

predictions = model.predict(X)

probabilities = model.predict_proba(X)[:, 1]

df["prediction"] = predictions

df["attack_probability"] = probabilities


# ---------------------------------------
# False Negatives
# ---------------------------------------

false_negatives = df[
    (df["label"] == 1) &
    (df["prediction"] == 0)
].copy()


# ---------------------------------------
# False Positives
# ---------------------------------------

false_positives = df[
    (df["label"] == 0) &
    (df["prediction"] == 1)
].copy()


# ---------------------------------------
# Print False Negatives
# ---------------------------------------

print("=" * 80)
print("FALSE NEGATIVES")
print("=" * 80)

print(f"Total: {len(false_negatives)}")

for _, row in false_negatives.iterrows():

    print("\n" + "-" * 80)

    print(
        f"Attack Probability: "
        f"{row['attack_probability']:.4f}"
    )

    print("Prompt:")

    print(row["prompt"][:1500])


# ---------------------------------------
# Print False Positives
# ---------------------------------------

print("\n\n" + "=" * 80)
print("FALSE POSITIVES")
print("=" * 80)

print(f"Total: {len(false_positives)}")

for _, row in false_positives.head(30).iterrows():

    print("\n" + "-" * 80)

    print(
        f"Attack Probability: "
        f"{row['attack_probability']:.4f}"
    )

    print("Prompt:")

    print(row["prompt"][:1500])