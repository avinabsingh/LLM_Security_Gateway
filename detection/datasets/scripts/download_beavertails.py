from datasets import load_dataset

print("=" * 60)
print("Downloading BeaverTails Dataset...")
print("=" * 60)

dataset = load_dataset(
    "PKU-Alignment/BeaverTails"
)

print("\nDataset Information")
print("-" * 60)
print(dataset)

print("\nColumns")
print("-" * 60)
print(dataset["330k_train"].column_names)

print("\nFirst Record")
print("-" * 60)
print(dataset["330k_train"][0])