import pandas as pd
import joblib

from pathlib import Path


# ---------------------------------------
# Project Root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


# ---------------------------------------
# Paths
# ---------------------------------------

FEATURE_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "hybrid_test_features.csv"
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

OUTPUT_PATH = (
    BASE_DIR
    / "evaluation"
    / "fusion"
    / "risk_fusion_test.csv"
)


# ---------------------------------------
# Load Feature Dataset
# ---------------------------------------

print("=" * 80)
print("LOADING HYBRID TEST FEATURES")
print("=" * 80)

df = pd.read_csv(
    FEATURE_PATH
)

print(
    f"Test samples: {len(df)}"
)


# ---------------------------------------
# Load Baseline Model
# ---------------------------------------

print("\n" + "=" * 80)
print("LOADING TF-IDF BASELINE")
print("=" * 80)

model = joblib.load(
    MODEL_PATH
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)

print("Baseline model loaded.")
print("TF-IDF vectorizer loaded.")


# ---------------------------------------
# TF-IDF Features
# ---------------------------------------

print("\n" + "=" * 80)
print("GENERATING TF-IDF RISK SCORES")
print("=" * 80)

X_tfidf = vectorizer.transform(
    df["prompt"]
)

print(
    f"TF-IDF matrix: {X_tfidf.shape}"
)


# ---------------------------------------
# Attack Probability
# ---------------------------------------

tfidf_probability = (
    model.predict_proba(X_tfidf)[:, 1]
)


df["tfidf_attack_probability"] = (
    tfidf_probability
)


# ---------------------------------------
# Reorder Columns
# ---------------------------------------

columns = [
    "prompt",

    "label",

    "tfidf_attack_probability",

    # Linguistic
    "char_length",
    "word_count",
    "question_marks",
    "exclamation_marks",
    "uppercase_letters",
    "digits",
    "special_characters",

    # Structural
    "instruction_override",
    "memory_reset",
    "developer_mode",
    "prompt_leakage",
    "information_extraction",
    "jailbreak",
    "role_change",
    "encoding",
    "authority_claim",
    "urgency_manipulation",

    # Semantic
    "attack_similarity",

    # Obfuscation
    "unicode_anomaly",
    "leetspeak",
    "symbol_substitution",
    "base64",
    "binary",
    "hexadecimal",
    "obfuscation_score"
]


df = df[
    columns
]


# ---------------------------------------
# Save
# ---------------------------------------

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------
# Report
# ---------------------------------------

print("\n" + "=" * 80)
print("RISK FUSION DATASET")
print("=" * 80)

print(
    f"Samples : {len(df)}"
)

print(
    f"Columns : {len(df.columns)}"
)

print(
    f"Shape   : {df.shape}"
)

print("\nLabel Distribution:")

print(
    df["label"].value_counts()
)

print("\nTF-IDF Probability Statistics:")

print(
    df["tfidf_attack_probability"].describe()
)

print("\nSaved to:")

print(
    OUTPUT_PATH
)