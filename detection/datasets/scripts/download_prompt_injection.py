from datasets import load_dataset

print("Downloading Prompt Injection Dataset...")

dataset = load_dataset(
    "cyberec/Prompt-injection-dataset",
    "core"
)

print(dataset)

print("\nColumns:")
print(dataset["train"].column_names)

print("\nFirst Record:")
print(dataset["train"][0])