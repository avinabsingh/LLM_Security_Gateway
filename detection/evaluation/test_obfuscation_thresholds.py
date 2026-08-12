import sys
from pathlib import Path

# ---------------------------------------
# Project root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(BASE_DIR)
)


import pandas as pd

from features.obfuscation import ObfuscationDetector


# ---------------------------------------
# Load Test Dataset
# ---------------------------------------

TEST_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "test.csv"
)


print("=" * 80)
print("LOADING TEST DATASET")
print("=" * 80)

df = pd.read_csv(TEST_PATH)

print(f"Total samples: {len(df)}")


# ---------------------------------------
# Initialize Detector
# ---------------------------------------

detector = ObfuscationDetector()


# ---------------------------------------
# Calculate Obfuscation Scores
# ---------------------------------------

print("\n" + "=" * 80)
print("CALCULATING OBFUSCATION SCORES")
print("=" * 80)

scores = []

for prompt in df["prompt"].astype(str):

    result = detector.analyze(prompt)

    scores.append(
        result["obfuscation_score"]
    )


df["obfuscation_score"] = scores


print("Obfuscation analysis completed.")


# ---------------------------------------
# Threshold Analysis
# ---------------------------------------

thresholds = [
    0.05,
    0.10,
    0.15,
    0.20,
    0.25
]


print("\n" + "=" * 80)
print("OBFUSCATION THRESHOLD ANALYSIS")
print("=" * 80)


for threshold in thresholds:

    flagged = (
        df["obfuscation_score"] >= threshold
    )

    actual_attacks = (
        df["label"] == 1
    )

    actual_safe = (
        df["label"] == 0
    )

    true_positives = (
        flagged & actual_attacks
    ).sum()

    false_negatives = (
        (~flagged) & actual_attacks
    ).sum()

    false_positives = (
        flagged & actual_safe
    ).sum()

    true_negatives = (
        (~flagged) & actual_safe
    ).sum()

    attack_total = actual_attacks.sum()

    safe_total = actual_safe.sum()

    attack_recall = (
        true_positives / attack_total
        if attack_total > 0
        else 0
    )

    safe_flag_rate = (
        false_positives / safe_total
        if safe_total > 0
        else 0
    )

    print("\n" + "-" * 80)

    print(
        f"Threshold: {threshold:.2f}"
    )

    print(
        f"True Positives   : {true_positives}"
    )

    print(
        f"False Negatives  : {false_negatives}"
    )

    print(
        f"False Positives  : {false_positives}"
    )

    print(
        f"True Negatives   : {true_negatives}"
    )

    print(
        f"Attack Recall    : {attack_recall:.4f}"
    )

    print(
        f"Safe Flag Rate   : {safe_flag_rate:.4f}"
    )


# ---------------------------------------
# Score Distribution
# ---------------------------------------

print("\n" + "=" * 80)
print("SCORE DISTRIBUTION")
print("=" * 80)

print(
    df["obfuscation_score"].describe()
)


# ---------------------------------------
# Highest Scoring Safe Prompts
# ---------------------------------------

print("\n" + "=" * 80)
print("TOP 10 SAFE PROMPTS BY OBFUSCATION SCORE")
print("=" * 80)

safe_prompts = (
    df[df["label"] == 0]
    .sort_values(
        "obfuscation_score",
        ascending=False
    )
    .head(10)
)


for _, row in safe_prompts.iterrows():

    print("\n" + "-" * 80)

    print(
        f"Score: "
        f"{row['obfuscation_score']:.4f}"
    )

    print(
        row["prompt"][:500]
    )


# ---------------------------------------
# Highest Scoring Attacks
# ---------------------------------------

print("\n" + "=" * 80)
print("TOP 10 ATTACKS BY OBFUSCATION SCORE")
print("=" * 80)

attack_prompts = (
    df[df["label"] == 1]
    .sort_values(
        "obfuscation_score",
        ascending=False
    )
    .head(10)
)


for _, row in attack_prompts.iterrows():

    print("\n" + "-" * 80)

    print(
        f"Score: "
        f"{row['obfuscation_score']:.4f}"
    )

    print(
        row["prompt"][:500]
    )