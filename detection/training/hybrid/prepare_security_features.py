import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(BASE_DIR))

import pandas as pd
from pathlib import Path

from features.extractor import ThreatFeatureExtractor


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
    / "train.csv"
)

OUTPUT_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "security_hybrid_train_features.csv"
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
# Load Training Data
# ---------------------------------------

print("=" * 80)
print("LOADING TRAINING DATA")
print("=" * 80)

df = pd.read_csv(
    TRAIN_PATH
)

print(
    f"Total training samples: {len(df)}"
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


    # Structural
    for feature in SECURITY_FEATURES:

        if feature in report["structural"]:

            feature_row[feature] = (
                report["structural"][feature]
            )


    # Semantic
    feature_row["attack_similarity"] = (
        report["semantic"]["attack_similarity"]
    )


    # Obfuscation
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
print("SECURITY FEATURE DATASET")
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