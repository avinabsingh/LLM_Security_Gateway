
from datasets import load_dataset

print("=" * 60)
print("Loading BeaverTails...")
print("=" * 60)

dataset = load_dataset("PKU-Alignment/BeaverTails")

train = dataset["30k_train"]   # Smaller subset for exploration

print("\nTotal Samples")
print("-" * 60)
print(len(train))


print("\nSafe vs Unsafe")
print("-" * 60)

safe = 0
unsafe = 0

for sample in train:

    if sample["is_safe"]:
        safe += 1
    else:
        unsafe += 1

print(f"Safe   : {safe}")
print(f"Unsafe : {unsafe}")


print("\nSample Unsafe Prompt")
print("-" * 60)

for sample in train:

    if not sample["is_safe"]:
        print(sample["prompt"])
        break


print("\nSample Safe Prompt")
print("-" * 60)

for sample in train:

    if sample["is_safe"]:
        print(sample["prompt"])
        break