import sys
from pathlib import Path

# ---------------------------------------
# Project Root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(BASE_DIR)
)


import pandas as pd

from features.extractor import ThreatFeatureExtractor
from features.feature_vector import FeatureVectorBuilder


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
    / "hybrid_test_features.csv"
)


# ---------------------------------------
# Load Data
# ---------------------------------------

print("=" * 80)
print("LOADING TEST DATA")
print("=" * 80)

df = pd.read_csv(TEST_PATH)

print(
    f"Total test samples: {len(df)}"
)


# ---------------------------------------
# Initialize
# ---------------------------------------

print("\n" + "=" * 80)
print("INITIALIZING FEATURE EXTRACTOR")
print("=" * 80)

extractor = ThreatFeatureExtractor()

builder = FeatureVectorBuilder()


# ---------------------------------------
# Extract Features
# ---------------------------------------

vectors = []

labels = []

prompts = []


print("\n" + "=" * 80)
print("EXTRACTING TEST FEATURES")
print("=" * 80)


for index, row in df.iterrows():

    prompt = str(
        row["prompt"]
    )

    label = int(
        row["label"]
    )

    report = extractor.extract(
        prompt
    )

    vector = builder.build(
        report
    )

    vectors.append(vector)

    labels.append(label)

    prompts.append(prompt)


    if (index + 1) % 500 == 0:

        print(
            f"Processed: {index + 1}/{len(df)}"
        )


# ---------------------------------------
# Create DataFrame
# ---------------------------------------

feature_names = (
    builder.get_feature_names()
)


feature_df = pd.DataFrame(
    vectors,
    columns=feature_names
)


feature_df["label"] = labels

feature_df["prompt"] = prompts


# ---------------------------------------
# Reorder
# ---------------------------------------

columns = (
    ["prompt"]
    + feature_names
    + ["label"]
)


feature_df = feature_df[
    columns
]


# ---------------------------------------
# Save
# ---------------------------------------

feature_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ---------------------------------------
# Report
# ---------------------------------------

print("\n" + "=" * 80)
print("TEST FEATURE EXTRACTION COMPLETE")
print("=" * 80)

print(
    f"Samples: {len(feature_df)}"
)

print(
    f"Features: {len(feature_names)}"
)

print(
    f"Shape: {feature_df.shape}"
)

print("\nLabel Distribution:")

print(
    feature_df["label"].value_counts()
)

print("\nSaved to:")

print(
    OUTPUT_PATH
)