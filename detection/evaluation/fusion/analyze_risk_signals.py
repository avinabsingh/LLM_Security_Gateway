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
# Signals
# ---------------------------------------

signals = [
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
    "obfuscation_score"
]


# ---------------------------------------
# Safe vs Attack Means
# ---------------------------------------

print("\n" + "=" * 80)
print("SAFE vs ATTACK SIGNAL DISTRIBUTION")
print("=" * 80)

distribution = (
    df.groupby("label")[signals]
    .mean()
    .T
)

distribution.columns = [
    "Safe",
    "Attack"
]

distribution["Difference"] = (
    distribution["Attack"]
    - distribution["Safe"]
)

distribution["Absolute Difference"] = (
    distribution["Difference"]
    .abs()
)

distribution = distribution.sort_values(
    "Absolute Difference",
    ascending=False
)

print(
    distribution.to_string()
)


# ---------------------------------------
# TF-IDF Distribution
# ---------------------------------------

print("\n" + "=" * 80)
print("TF-IDF PROBABILITY BY LABEL")
print("=" * 80)

print(
    df.groupby("label")[
        "tfidf_attack_probability"
    ].describe()
)


# ---------------------------------------
# Semantic Distribution
# ---------------------------------------

print("\n" + "=" * 80)
print("SEMANTIC SIMILARITY BY LABEL")
print("=" * 80)

print(
    df.groupby("label")[
        "attack_similarity"
    ].describe()
)


# ---------------------------------------
# Obfuscation Distribution
# ---------------------------------------

print("\n" + "=" * 80)
print("OBFUSCATION SCORE BY LABEL")
print("=" * 80)

print(
    df.groupby("label")[
        "obfuscation_score"
    ].describe()
)


# ---------------------------------------
# High TF-IDF / Low TF-IDF
# ---------------------------------------

print("\n" + "=" * 80)
print("HIGH TF-IDF EXAMPLES")
print("=" * 80)

high_tfidf = df.sort_values(
    "tfidf_attack_probability",
    ascending=False
).head(15)

for _, row in high_tfidf.iterrows():

    print(
        f"\nLabel: {row['label']}"
    )

    print(
        f"TF-IDF: {row['tfidf_attack_probability']:.4f}"
    )

    print(
        f"Semantic: {row['attack_similarity']:.4f}"
    )

    print(
        f"Obfuscation: {row['obfuscation_score']:.4f}"
    )

    print(
        f"Prompt: {row['prompt'][:300]}"
    )


# ---------------------------------------
# High Obfuscation Examples
# ---------------------------------------

print("\n" + "=" * 80)
print("HIGH OBFUSCATION EXAMPLES")
print("=" * 80)

high_obfuscation = df.sort_values(
    "obfuscation_score",
    ascending=False
).head(15)

for _, row in high_obfuscation.iterrows():

    print(
        f"\nLabel: {row['label']}"
    )

    print(
        f"Obfuscation: {row['obfuscation_score']:.4f}"
    )

    print(
        f"TF-IDF: {row['tfidf_attack_probability']:.4f}"
    )

    print(
        f"Semantic: {row['attack_similarity']:.4f}"
    )

    print(
        f"Prompt: {row['prompt'][:300]}"
    )


# ---------------------------------------
# High Semantic Similarity
# ---------------------------------------

print("\n" + "=" * 80)
print("HIGH SEMANTIC SIMILARITY EXAMPLES")
print("=" * 80)

high_semantic = df.sort_values(
    "attack_similarity",
    ascending=False
).head(15)

for _, row in high_semantic.iterrows():

    print(
        f"\nLabel: {row['label']}"
    )

    print(
        f"Semantic: {row['attack_similarity']:.4f}"
    )

    print(
        f"TF-IDF: {row['tfidf_attack_probability']:.4f}"
    )

    print(
        f"Obfuscation: {row['obfuscation_score']:.4f}"
    )

    print(
        f"Prompt: {row['prompt'][:300]}"
    )