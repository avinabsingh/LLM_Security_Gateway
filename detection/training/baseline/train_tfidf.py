import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


# ---------------------------------------
# Paths
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "train.csv"
)


# ---------------------------------------
# Load Training Data
# ---------------------------------------

print("=" * 60)
print("Loading Training Data")
print("=" * 60)

df = pd.read_csv(TRAIN_PATH)

print(f"Training samples: {len(df)}")


# ---------------------------------------
# TF-IDF Vectorizer
# ---------------------------------------

print("\n" + "=" * 60)
print("Creating TF-IDF Features")
print("=" * 60)

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)


X_train = vectorizer.fit_transform(
    df["prompt"].astype(str)
)

y_train = df["label"]


# ---------------------------------------
# Information
# ---------------------------------------

print(f"\nNumber of samples : {X_train.shape[0]}")
print(f"Number of features: {X_train.shape[1]}")
print(f"Matrix shape      : {X_train.shape}")


# ---------------------------------------
# Vocabulary Sample
# ---------------------------------------

features = vectorizer.get_feature_names_out()

print("\nFirst 30 TF-IDF Features:")

for feature in features[:30]:
    print(feature)


# ---------------------------------------
# Sample Vector
# ---------------------------------------

print("\nFirst Prompt:")
print(df.iloc[0]["prompt"])

print("\nNon-zero TF-IDF values:")

row = X_train[0]

print(row)