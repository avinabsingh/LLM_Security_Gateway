import sys
from pathlib import Path
from tqdm import tqdm
from transformers import pipeline
import pandas as pd

# ---------------------------------------
# Project Root
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from features.extractor import ThreatFeatureExtractor
from features.feature_vector import FeatureVectorBuilder

# ---------------------------------------
# Paths
# ---------------------------------------
TRAIN_PATH = BASE_DIR / "training" / "artifacts" / "train.csv"
OUTPUT_PATH = BASE_DIR / "training" / "artifacts" / "hybrid_train_features.csv"

# ---------------------------------------
# Load Data
# ---------------------------------------
print("=" * 80)
print("LOADING TRAINING DATA")
print("=" * 80)

df = pd.read_csv(TRAIN_PATH)

# OPTIONAL: Uncomment the line below for a fast 1-minute test to verify the pipeline works
# df = df.sample(1000, random_state=42) 

print(f"Total training samples to process: {len(df)}")

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
    device=-1  # Set to 0 if using a GPU
)

extractor = ThreatFeatureExtractor()
builder = FeatureVectorBuilder()

def get_transformer_probability(text):
    result = baseline_model(str(text), truncation=True, max_length=512)[0]
    return float(result["score"]) if result["label"] == "INJECTION" else float(1.0 - result["score"])

# ---------------------------------------
# Extract Features
# ---------------------------------------
vectors = []
labels = []
prompts = []

print("\n" + "=" * 80)
print("EXTRACTING FEATURES (OPTIMIZED)")
print("=" * 80)

for row in tqdm(df.itertuples(index=False), total=len(df), desc="Processing Prompts"):
    prompt = str(row.prompt)
    label = int(row.label)

    baseline_prob = get_transformer_probability(prompt)
    report = extractor.extract(prompt)
    hybrid_vector = builder.build(report)
    
    # Creates the 26-feature vector
    final_vector = [baseline_prob] + hybrid_vector

    vectors.append(final_vector)
    labels.append(label)
    prompts.append(prompt)

# ---------------------------------------
# Create DataFrame & Save
# ---------------------------------------
feature_names = ["baseline_attack_probability"] + builder.get_feature_names()
feature_df = pd.DataFrame(vectors, columns=feature_names)
feature_df["label"] = labels
feature_df["prompt"] = prompts

columns = ["prompt"] + feature_names + ["label"]
feature_df = feature_df[columns]

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
feature_df.to_csv(OUTPUT_PATH, index=False)

print("\n" + "=" * 80)
print("FEATURE EXTRACTION COMPLETE")
print("=" * 80)
print(f"Shape: {feature_df.shape}")
print(f"Saved to: {OUTPUT_PATH}")