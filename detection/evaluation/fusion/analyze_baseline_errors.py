import pandas as pd
from pathlib import Path


# ---------------------------------------
# Project Root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "evaluation"
    / "fusion"
    / "risk_fusion_test.csv"
)


# ---------------------------------------
# Load Dataset
# ---------------------------------------

print("=" * 80)
print("LOADING RISK FUSION DATASET")
print("=" * 80)

df = pd.read_csv(DATA_PATH)

print(
    f"Samples: {len(df)}"
)


# ---------------------------------------
# Baseline Predictions
# ---------------------------------------

# The baseline model used approximately 0.5
# as its classification threshold.

df["baseline_prediction"] = (
    df["tfidf_attack_probability"] >= 0.5
).astype(int)


# ---------------------------------------
# Error Types
# ---------------------------------------

false_negatives = df[
    (df["label"] == 1) &
    (df["baseline_prediction"] == 0)
]

false_positives = df[
    (df["label"] == 0) &
    (df["baseline_prediction"] == 1)
]

true_positives = df[
    (df["label"] == 1) &
    (df["baseline_prediction"] == 1)
]

true_negatives = df[
    (df["label"] == 0) &
    (df["baseline_prediction"] == 0)
]


# ---------------------------------------
# Summary
# ---------------------------------------

print("\n" + "=" * 80)
print("BASELINE ERROR SUMMARY")
print("=" * 80)

print(
    f"True Positives  : {len(true_positives)}"
)

print(
    f"False Negatives : {len(false_negatives)}"
)

print(
    f"False Positives : {len(false_positives)}"
)

print(
    f"True Negatives  : {len(true_negatives)}"
)


# ---------------------------------------
# False Negatives
# ---------------------------------------

print("\n" + "=" * 80)
print("FALSE NEGATIVES")
print("=" * 80)

print(
    f"Total: {len(false_negatives)}"
)


fn_columns = [
    "label",
    "tfidf_attack_probability",
    "attack_similarity",
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
    "unicode_anomaly",
    "leetspeak",
    "symbol_substitution",
    "base64",
    "binary",
    "hexadecimal",
    "obfuscation_score",
    "prompt"
]


# Sort by TF-IDF confidence,
# starting with the attacks the baseline
# was most confident were SAFE.

fn_sorted = false_negatives.sort_values(
    "tfidf_attack_probability"
)


for index, (_, row) in enumerate(
    fn_sorted.head(30).iterrows(),
    start=1
):

    print("\n" + "-" * 80)

    print(
        f"FALSE NEGATIVE #{index}"
    )

    print(
        f"TF-IDF probability : "
        f"{row['tfidf_attack_probability']:.4f}"
    )

    print(
        f"Semantic similarity: "
        f"{row['attack_similarity']:.4f}"
    )

    print(
        f"Obfuscation score   : "
        f"{row['obfuscation_score']:.4f}"
    )

    print(
        f"Instruction override: "
        f"{row['instruction_override']}"
    )

    print(
        f"Prompt leakage      : "
        f"{row['prompt_leakage']}"
    )

    print(
        f"Information extract : "
        f"{row['information_extraction']}"
    )

    print(
        f"Jailbreak           : "
        f"{row['jailbreak']}"
    )

    print(
        f"Encoding            : "
        f"{row['encoding']}"
    )

    print(
        f"Unicode anomaly     : "
        f"{row['unicode_anomaly']:.4f}"
    )

    print(
        f"Leetspeak           : "
        f"{row['leetspeak']:.4f}"
    )

    print(
        f"Prompt: {str(row['prompt'])[:500]}"
    )


# ---------------------------------------
# False Positives
# ---------------------------------------

print("\n" + "=" * 80)
print("FALSE POSITIVES")
print("=" * 80)

print(
    f"Total: {len(false_positives)}"
)


fp_sorted = false_positives.sort_values(
    "tfidf_attack_probability",
    ascending=False
)


for index, (_, row) in enumerate(
    fp_sorted.head(30).iterrows(),
    start=1
):

    print("\n" + "-" * 80)

    print(
        f"FALSE POSITIVE #{index}"
    )

    print(
        f"TF-IDF probability : "
        f"{row['tfidf_attack_probability']:.4f}"
    )

    print(
        f"Semantic similarity: "
        f"{row['attack_similarity']:.4f}"
    )

    print(
        f"Obfuscation score   : "
        f"{row['obfuscation_score']:.4f}"
    )

    print(
        f"Prompt leakage      : "
        f"{row['prompt_leakage']}"
    )

    print(
        f"Information extract : "
        f"{row['information_extraction']}"
    )

    print(
        f"Jailbreak           : "
        f"{row['jailbreak']}"
    )

    print(
        f"Prompt: {str(row['prompt'])[:500]}"
    )


# ---------------------------------------
# Security Signals in False Negatives
# ---------------------------------------

print("\n" + "=" * 80)
print("FALSE NEGATIVES WITH SECURITY SIGNALS")
print("=" * 80)


security_columns = [
    "instruction_override",
    "memory_reset",
    "developer_mode",
    "prompt_leakage",
    "information_extraction",
    "jailbreak",
    "role_change",
    "encoding",
    "authority_claim",
    "urgency_manipulation"
]


fn_security = false_negatives[
    security_columns
].sum().sort_values(
    ascending=False
)


print(fn_security)


# ---------------------------------------
# Obfuscation in False Negatives
# ---------------------------------------

print("\n" + "=" * 80)
print("OBFUSCATION IN FALSE NEGATIVES")
print("=" * 80)

obfuscation_columns = [
    "unicode_anomaly",
    "leetspeak",
    "symbol_substitution",
    "base64",
    "binary",
    "hexadecimal",
    "obfuscation_score"
]


print(
    false_negatives[
        obfuscation_columns
    ].describe()
)


# ---------------------------------------
# Semantic Similarity in False Negatives
# ---------------------------------------

print("\n" + "=" * 80)
print("SEMANTIC SIMILARITY IN FALSE NEGATIVES")
print("=" * 80)

print(
    false_negatives[
        "attack_similarity"
    ].describe()
)