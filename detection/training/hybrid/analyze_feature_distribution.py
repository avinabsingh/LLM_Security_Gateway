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
    / "hybrid_train_features.csv"
)


# ---------------------------------------
# Load
# ---------------------------------------

print("=" * 80)
print("LOADING HYBRID TRAINING FEATURES")
print("=" * 80)

df = pd.read_csv(
    FEATURE_PATH
)


feature_columns = [
    column
    for column in df.columns
    if column not in [
        "prompt",
        "label"
    ]
]


# ---------------------------------------
# Mean by class
# ---------------------------------------

print("\n" + "=" * 80)
print("FEATURE MEANS BY CLASS")
print("=" * 80)

means = (
    df.groupby("label")[feature_columns]
    .mean()
    .T
)

means.columns = [
    "Safe",
    "Attack"
]


means["Difference"] = (
    means["Attack"]
    - means["Safe"]
)


means["Absolute Difference"] = (
    means["Difference"].abs()
)


means = means.sort_values(
    "Absolute Difference",
    ascending=False
)


print(
    means.to_string()
)


# ---------------------------------------
# Attack/Safe non-zero rates
# ---------------------------------------

print("\n" + "=" * 80)
print("NON-ZERO RATE BY CLASS")
print("=" * 80)


nonzero = (
    df.groupby("label")[feature_columns]
    .apply(
        lambda x: (x != 0).mean()
    )
    .T
)

nonzero.columns = [
    "Safe",
    "Attack"
]


nonzero["Difference"] = (
    nonzero["Attack"]
    - nonzero["Safe"]
)


nonzero["Absolute Difference"] = (
    nonzero["Difference"].abs()
)


nonzero = nonzero.sort_values(
    "Absolute Difference",
    ascending=False
)


print(
    nonzero.to_string()
)


# ---------------------------------------
# Special Character Analysis
# ---------------------------------------

print("\n" + "=" * 80)
print("SPECIAL CHARACTER ANALYSIS")
print("=" * 80)

print(
    df.groupby("label")[
        "special_characters"
    ].describe()
)


# ---------------------------------------
# Uppercase Analysis
# ---------------------------------------

print("\n" + "=" * 80)
print("UPPERCASE ANALYSIS")
print("=" * 80)

print(
    df.groupby("label")[
        "uppercase_letters"
    ].describe()
)


# ---------------------------------------
# Obfuscation Analysis
# ---------------------------------------

print("\n" + "=" * 80)
print("OBFUSCATION SCORE ANALYSIS")
print("=" * 80)

print(
    df.groupby("label")[
        "obfuscation_score"
    ].describe()
)