import pandas as pd
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


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

MODEL_DIR = (
    BASE_DIR
    / "models"
    / "baseline"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ---------------------------------------
# Load Training Data
# ---------------------------------------

print("=" * 60)
print("Loading Training Data")
print("=" * 60)

df = pd.read_csv(TRAIN_PATH)

X_text = df["prompt"].astype(str)
y = df["label"]

print(f"Training samples: {len(df)}")

print("\nLabel Distribution")
print(y.value_counts())


# ---------------------------------------
# TF-IDF
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

X = vectorizer.fit_transform(X_text)

print(f"Feature Matrix: {X.shape}")


# ---------------------------------------
# Logistic Regression
# ---------------------------------------

print("\n" + "=" * 60)
print("Training Logistic Regression")
print("=" * 60)

model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000,
    random_state=42
)

model.fit(X, y)

print("Model training completed.")


# ---------------------------------------
# Save Model
# ---------------------------------------

model_path = MODEL_DIR / "logistic_regression.joblib"

vectorizer_path = MODEL_DIR / "tfidf_vectorizer.joblib"

joblib.dump(
    model,
    model_path
)

joblib.dump(
    vectorizer,
    vectorizer_path
)


print("\n" + "=" * 60)
print("MODEL SAVED")
print("=" * 60)

print(f"Model      : {model_path}")
print(f"Vectorizer : {vectorizer_path}")