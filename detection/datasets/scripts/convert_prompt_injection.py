from datasets import load_dataset
import pandas as pd
from pathlib import Path


print("Loading dataset...")

dataset = load_dataset(
    "cyberec/Prompt-injection-dataset",
    "core"
)

train = dataset["train"]

rows = []

for idx, sample in enumerate(train):

    rows.append({

        "id": idx,

        "prompt": sample["text"],

        "binary_label": sample["label"],

        "attack_category": sample["category"],

        "severity": sample["severity"],

        "source_dataset": "cyberec"

    })

df = pd.DataFrame(rows)

print(df.head())


output_dir = (
    Path(__file__).resolve().parent.parent
    / "processed"
)

output_dir.mkdir(
    parents=True,
    exist_ok=True
)

output_file = output_dir / "master_prompt_injection.csv"

df.to_csv(
    output_file,
    index=False
)

print("\nSaved to:")
print(output_file)