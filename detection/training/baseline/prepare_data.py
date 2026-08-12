import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split


# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR
    / "datasets"
    / "processed"
    / "training_dataset.csv"
)

OUTPUT_DIR = BASE_DIR / "training" / "artifacts"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# Load Dataset
# ---------------------------------------

print("=" * 60)
print("Loading Training Dataset")
print("=" * 60)

df = pd.read_csv(DATASET_PATH)

print(f"Total samples: {len(df)}")


# ---------------------------------------
# Remove duplicates
# ---------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["prompt"]
).reset_index(drop=True)

after = len(df)

print(f"Duplicates removed: {before - after}")
print(f"Samples after cleaning: {after}")


# ---------------------------------------
# Train/Test Split
# ---------------------------------------

train, test = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["label"]
)


# ---------------------------------------
# Save datasets
# ---------------------------------------

train_path = OUTPUT_DIR / "train.csv"
test_path = OUTPUT_DIR / "test.csv"

train.to_csv(
    train_path,
    index=False
)

test.to_csv(
    test_path,
    index=False
)


# ---------------------------------------
# Print Information
# ---------------------------------------

print("\n" + "=" * 60)
print("DATASET SPLIT")
print("=" * 60)

print(f"Training samples: {len(train)}")
print(f"Testing samples : {len(test)}")


print("\nTraining Label Distribution")
print(train["label"].value_counts())


print("\nTesting Label Distribution")
print(test["label"].value_counts())


print("\nSaved:")
print(train_path)
print(test_path)