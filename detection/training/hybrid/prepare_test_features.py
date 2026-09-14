import sys
from pathlib import Path
from tqdm import tqdm
from transformers import pipeline

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

print(f"Total test samples: {len(df)}")

# ---------------------------------------
# Initialize AI Models & Extractors
# ---------------------------------------
print("\n" + "=" * 80)
print("INITIALIZING EXTRACTORS & TRANSFORMER BASELINE")
print("=" * 80)

print("Loading Hugging Face DeBERTa-v3 Model (May take a moment)...")
baseline_model = pipeline(
    "text-classification",
    model="ProtectAI/deberta-v3-base-prompt-injection-v2",
    device=-1  # Set to 0 if you are using a dedicated GPU
)

extractor = ThreatFeatureExtractor()
builder = FeatureVectorBuilder()

# ---------------------------------------
# Helper Function for Baseline
# ---------------------------------------
def get_transformer_probability(text):
    result = baseline_model(str(text), truncation=True, max_length=512)[0]
    if result["label"] == "INJECTION":
        return float(result["score"])
    return float(1.0 - result["score"])

# ---------------------------------------
# Extract Features
# ---------------------------------------
vectors = []
labels = []
prompts = []

print("\n" + "=" * 80)
print("EXTRACTING TEST FEATURES (OPTIMIZED)")
print("=" * 80)

for row in tqdm(df.itertuples(index=False), total=len(df), desc="Processing Test Prompts"):
    prompt = str(row.prompt)
    label = int(row.label)

    # 1. Get Baseline Probability
    baseline_prob = get_transformer_probability(prompt)

    # 2. Get 25 Hybrid Features
    report = extractor.extract(prompt)
    hybrid_vector = builder.build(report)

    # 3. Fuse into the final 26-feature vector
    final_vector = [baseline_prob] + hybrid_vector

    vectors.append(final_vector)
    labels.append(label)
    prompts.append(prompt)

# ---------------------------------------
# Create DataFrame
# ---------------------------------------
feature_names = ["baseline_attack_probability"] + builder.get_feature_names()

feature_df = pd.DataFrame(
    vectors,
    columns=feature_names
)

feature_df["label"] = labels
feature_df["prompt"] = prompts

# ---------------------------------------
# Reorder Columns
# ---------------------------------------
columns = (
    ["prompt"]
    + feature_names
    + ["label"]
)

feature_df = feature_df[columns]

# ---------------------------------------
# Save
# ---------------------------------------
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

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

print(f"Samples: {len(feature_df)}")
print(f"Features: {len(feature_names)}")
print(f"Shape: {feature_df.shape}")
print("\nLabel Distribution:")
print(feature_df["label"].value_counts())
print(f"\nSaved to:\n{OUTPUT_PATH}")

