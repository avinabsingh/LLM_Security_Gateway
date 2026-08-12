import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import pandas as pd
import joblib

from features.obfuscation import ObfuscationDetector


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


# ---------------------------------------
# Load Test Data
# ---------------------------------------

df = pd.read_csv(TEST_PATH)


# ---------------------------------------
# Load Model
# ---------------------------------------

import joblib

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

model = joblib.load(MODEL_PATH)

vectorizer = joblib.load(VECTORIZER_PATH)


# ---------------------------------------
# Baseline Predictions
# ---------------------------------------

X = vectorizer.transform(
    df["prompt"].astype(str)
)

df["prediction"] = model.predict(X)

df["probability"] = model.predict_proba(X)[:, 1]


# ---------------------------------------
# Find False Negatives
# ---------------------------------------

false_negatives = df[
    (df["label"] == 1) &
    (df["prediction"] == 0)
].copy()


print("=" * 80)
print("FALSE NEGATIVES + OBFUSCATION ANALYSIS")
print("=" * 80)

print(f"False negatives: {len(false_negatives)}")


# ---------------------------------------
# Obfuscation Detector
# ---------------------------------------

detector = ObfuscationDetector()


# ---------------------------------------
# Analyze
# ---------------------------------------

for index, row in false_negatives.iterrows():

    prompt = row["prompt"]

    result = detector.analyze(prompt)

    print("\n" + "-" * 80)

    print(
        f"Attack probability: "
        f"{row['probability']:.4f}"
    )

    print(
        f"Obfuscation score: "
        f"{result['obfuscation_score']:.4f}"
    )

    print("\nPrompt:")

    print(prompt[:1000])

    print("\nObfuscation signals:")

    for key, value in result.items():

        if key != "obfuscation_score":

            print(
                f"{key}: {value}"
            )