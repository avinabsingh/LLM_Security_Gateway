import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET = BASE_DIR / "processed" / "training_dataset.csv"

df = pd.read_csv(DATASET)

print("=" * 60)
print("DATASET QUALITY REPORT")
print("=" * 60)

print(f"Total Samples : {len(df)}")

print(f"Duplicate Prompts : {df['prompt'].duplicated().sum()}")

print(f"Missing Prompts : {df['prompt'].isnull().sum()}")

print(f"Missing Labels : {df['label'].isnull().sum()}")

empty = (df["prompt"].astype(str).str.strip() == "").sum()

print(f"Empty Prompts : {empty}")

lengths = df["prompt"].astype(str).str.len()

print(f"Shortest Prompt : {lengths.min()}")

print(f"Longest Prompt : {lengths.max()}")

print(f"Average Length : {lengths.mean():.2f}")