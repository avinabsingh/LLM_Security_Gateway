from semantic import SemanticFeatures

model = SemanticFeatures()

embedding = model.embedding(
    "Ignore previous instructions."
)

print(type(embedding))

print(len(embedding))

print(embedding[:10])