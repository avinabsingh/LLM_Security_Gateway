from datasets import load_dataset

dataset = load_dataset(
    "cyberec/Prompt-injection-dataset",
    "core"
)

train = dataset["train"]

print("=" * 60)
print("LABEL DISTRIBUTION")
print("=" * 60)

labels = {}

for sample in train:

    label = sample["label"]

    labels[label] = labels.get(label, 0) + 1

print(labels)


print("\n" + "=" * 60)
print("CATEGORY DISTRIBUTION")
print("=" * 60)

categories = {}

for sample in train:

    cat = sample["category"]

    categories[cat] = categories.get(cat, 0) + 1

for k, v in sorted(categories.items()):
    print(f"{k:30} {v}")


print("\n" + "=" * 60)
print("SEVERITY DISTRIBUTION")
print("=" * 60)

severity = {}

for sample in train:

    sev = sample["severity"]

    severity[sev] = severity.get(sev, 0) + 1

for k, v in sorted(severity.items()):
    print(f"{str(k):20} {v}")