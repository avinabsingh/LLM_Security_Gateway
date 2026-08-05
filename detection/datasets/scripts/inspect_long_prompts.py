import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET = BASE_DIR / "processed" / "training_dataset.csv"

df = pd.read_csv(DATASET)

# Add prompt length
df["length"] = df["prompt"].astype(str).str.len()

# Top 5 longest prompts
longest = df.sort_values("length", ascending=False).head(5)

print("=" * 80)
print("TOP 5 LONGEST PROMPTS")
print("=" * 80)

for i, row in longest.iterrows():

    print("\n" + "-" * 80)
    print(f"Length : {row['length']}")
    print(f"Label  : {row['label']}")
    print(f"Source : {row['source']}")
    print("\nPrompt Preview:\n")

    print(row["prompt"][:1000])   # Show first 1000 characters only

    print("\n...")