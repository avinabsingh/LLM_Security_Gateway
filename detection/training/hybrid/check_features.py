import pandas as pd
from pathlib import Path


# ---------------------------------------
# Project Root
# ---------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]


FEATURE_PATH = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "hybrid_features_test.csv"
)


# ---------------------------------------
# Load
# ---------------------------------------

print("=" * 80)
print("LOADING HYBRID FEATURE DATASET")
print("=" * 80)

df = pd.read_csv(FEATURE_PATH)


# ---------------------------------------
# Basic Information
# ---------------------------------------

print("\nShape:")
print(df.shape)


print("\nColumns:")
print(df.columns.tolist())


print("\nFirst 5 Rows:")
print(df.head())


# ---------------------------------------
# Missing Values
# ---------------------------------------

print("\n" + "=" * 80)
print("MISSING VALUES")
print("=" * 80)

missing = df.isnull().sum()

print(
    missing[missing > 0]
)


# ---------------------------------------
# Label Distribution
# ---------------------------------------

print("\n" + "=" * 80)
print("LABEL DISTRIBUTION")
print("=" * 80)

print(
    df["label"].value_counts()
)


# ---------------------------------------
# Feature Statistics
# ---------------------------------------

feature_columns = [
    column
    for column in df.columns
    if column not in ["prompt", "label"]
]


print("\n" + "=" * 80)
print("FEATURE STATISTICS")
print("=" * 80)

print(
    df[feature_columns].describe().T
)


# ---------------------------------------
# Data Types
# ---------------------------------------

print("\n" + "=" * 80)
print("DATA TYPES")
print("=" * 80)

print(
    df.dtypes
)


# ---------------------------------------
# Constant Features
# ---------------------------------------

print("\n" + "=" * 80)
print("CONSTANT FEATURES")
print("=" * 80)

constant_features = []

for column in feature_columns:

    if df[column].nunique() <= 1:

        constant_features.append(column)


if constant_features:

    for feature in constant_features:

        print(feature)

else:

    print("No constant features found.")


# ---------------------------------------
# Final Validation
# ---------------------------------------

print("\n" + "=" * 80)
print("VALIDATION")
print("=" * 80)

print(
    f"Rows              : {len(df)}"
)

print(
    f"Feature columns   : {len(feature_columns)}"
)

print(
    f"Missing values    : {df.isnull().sum().sum()}"
)

print(
    f"Duplicate rows    : {df.duplicated().sum()}"
)