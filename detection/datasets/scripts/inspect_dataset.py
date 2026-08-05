from datasets import load_dataset

print("=" * 60)
print("Loading Alpaca Dataset...")
print("=" * 60)

dataset = load_dataset("yahma/alpaca-cleaned")

print("\nDataset Information")
print("-" * 60)

print(dataset)

print("\nTraining Split")
print("-" * 60)

print(dataset["train"])

print("\nColumns")
print("-" * 60)

print(dataset["train"].column_names)

print("\nFirst Record")
print("-" * 60)

print(dataset["train"][0])