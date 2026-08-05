import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

processed_dir = BASE_DIR / "processed"


print("=" * 60)
print("Loading datasets...")
print("=" * 60)

alpaca = pd.read_csv(
    processed_dir / "unified_alpaca.csv"
)

prompt = pd.read_csv(
    processed_dir / "master_prompt_injection.csv"
)


# ----------------------------------
# Convert Alpaca
# ----------------------------------

alpaca_df = pd.DataFrame({

    "prompt": alpaca["prompt"],

    "label": 0,

    "source": "alpaca"

})


# ----------------------------------
# Convert Prompt Injection Dataset
# ----------------------------------

prompt_df = pd.DataFrame({

    "prompt": prompt["prompt"],

    "label": prompt["binary_label"],

    "source": "cyberec"

})


# ----------------------------------
# Merge
# ----------------------------------

merged = pd.concat(
    [alpaca_df, prompt_df],
    ignore_index=True
)

merged = merged.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


print("\nMerged Dataset Shape")
print(merged.shape)

print("\nLabel Distribution")
print(merged["label"].value_counts())

print("\nFirst Five Rows")
print(merged.head())


output = processed_dir / "training_dataset.csv"

merged.to_csv(
    output,
    index=False
)

print("\nSaved to")
print(output)