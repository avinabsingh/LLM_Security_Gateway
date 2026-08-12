import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

import pandas as pd

from features.extractor import ThreatFeatureExtractor


# ---------------------------------------
# Paths
# ---------------------------------------

TEST_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "test.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "security_hybrid_test_features.csv"
)


# ---------------------------------------
# Security Features
# ---------------------------------------

SECURITY_FEATURES = [

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


# ---------------------------------------
# Load Test Data
# ---------------------------------------

print("=" * 80)
print("LOADING TEST DATA")
print("=" * 80)

df = pd.read_csv(
    TEST_PATH
)

print(
    f"Total test samples: {len(df)}"
)


# ---------------------------------------
# Initialize Extractor
# ---------------------------------------

extractor = ThreatFeatureExtractor()


# ---------------------------------------
# Extract Features
# ---------------------------------------

rows = []


for index, row in df.iterrows():

    prompt = row["prompt"]
    label = row["label"]

    report = extractor.extract(
        prompt
    )

    feature_row = {
        "prompt": prompt
    }

    # Structural features
    for feature in [
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
    ]:

        feature_row[feature] = (
            report["structural"][feature]
        )

    # Semantic feature
    feature_row["attack_similarity"] = (
        report["semantic"]["attack_similarity"]
    )

    # Obfuscation features
    for feature in [
        "unicode_anomaly",
        "leetspeak",
        "symbol_substitution",
        "base64",
        "binary",
        "hexadecimal",
        "obfuscation_score"
    ]:

        feature_row[feature] = (
            report["obfuscation"][feature]
        )

    feature_row["label"] = label

    rows.append(
        feature_row
    )

    if (index + 1) % 500 == 0:

        print(
            f"Processed: {index + 1}/{len(df)}"
        )


# ---------------------------------------
# Create DataFrame
# ---------------------------------------

result = pd.DataFrame(
    rows
)


# ---------------------------------------
# Save
# ---------------------------------------

result.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------
# Report
# ---------------------------------------

print("\n" + "=" * 80)
print("SECURITY TEST FEATURE DATASET")
print("=" * 80)

print(
    f"Samples  : {len(result)}"
)

print(
    f"Features : {len(SECURITY_FEATURES)}"
)

print(
    f"Shape    : {result.shape}"
)

print("\nLabel Distribution:")

print(
    result["label"].value_counts()
)

print("\nSaved to:")

print(
    OUTPUT_PATH
)