import pandas as pd
import numpy as np

from pathlib import Path
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from joblib import load


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

TRAIN_DATA = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "train.csv"
)

HYBRID_FEATURES = (
    BASE_DIR
    / "training"
    / "artifacts"
    / "hybrid_train_features.csv"
)

VECTORIZER_PATH = (
    BASE_DIR
    / "models"
    / "baseline"
    / "tfidf_vectorizer.joblib"
)

OUTPUT_PATH = (
    BASE_DIR
    / "evaluation"
    / "fusion"
    / "risk_fusion_train.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 80)
print("LOADING RISK FUSION TRAINING DATA")
print("=" * 80)

train_df = pd.read_csv(TRAIN_DATA)

hybrid_df = pd.read_csv(HYBRID_FEATURES)

print(f"Training samples       : {len(train_df)}")
print(f"Hybrid feature samples : {len(hybrid_df)}")


# ============================================================
# BASIC CHECK
# ============================================================

if len(train_df) != len(hybrid_df):
    raise ValueError(
        "Training data and hybrid feature data have different row counts."
    )

if not train_df["prompt"].equals(hybrid_df["prompt"]):
    raise ValueError(
        "Prompt order does not match between training data and hybrid features."
    )

print("Prompt alignment check: PASSED")


# ============================================================
# LOAD TF-IDF VECTORIZER
# ============================================================

print("\nLoading TF-IDF vectorizer...")

vectorizer = load(VECTORIZER_PATH)

X_tfidf = vectorizer.transform(train_df["prompt"])

y = train_df["label"].values

print(f"TF-IDF matrix: {X_tfidf.shape}")


# ============================================================
# OUT-OF-FOLD TF-IDF PROBABILITIES
# ============================================================

print("\nGenerating out-of-fold TF-IDF probabilities...")

oof_probability = np.zeros(len(train_df))

skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


for fold, (train_idx, val_idx) in enumerate(
    skf.split(X_tfidf, y),
    start=1
):

    print(f"\nFold {fold}/5")

    X_fold_train = X_tfidf[train_idx]
    X_fold_val = X_tfidf[val_idx]

    y_fold_train = y[train_idx]

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    model.fit(
        X_fold_train,
        y_fold_train
    )

    probabilities = model.predict_proba(
        X_fold_val
    )[:, 1]

    oof_probability[val_idx] = probabilities

    print(
        f"Validation samples: {len(val_idx)}"
    )


# ============================================================
# CHECK OOF PROBABILITIES
# ============================================================

print("\n" + "=" * 80)
print("OOF TF-IDF PROBABILITY STATISTICS")
print("=" * 80)

print(
    pd.Series(oof_probability).describe()
)


# ============================================================
# GET HYBRID FEATURES
# ============================================================

feature_columns = [
    "char_length",
    "word_count",
    "question_marks",
    "exclamation_marks",
    "uppercase_letters",
    "digits",
    "special_characters",

    "instruction_override",
    "memory_reset",
    "developer_mode",
    "prompt_leakage",
    "information_extraction",
    "jailbreak",
    "role_change",
    "encoding",
    "authority_claim",
    "urgency_manipulation",

    "attack_similarity",

    "unicode_anomaly",
    "leetspeak",
    "symbol_substitution",
    "base64",
    "binary",
    "hexadecimal",
    "obfuscation_score"
]


missing = [
    col
    for col in feature_columns
    if col not in hybrid_df.columns
]

if missing:
    raise ValueError(
        f"Missing hybrid features: {missing}"
    )


# ============================================================
# BUILD FUSION DATASET
# ============================================================

fusion_df = hybrid_df[
    ["prompt"] + feature_columns + ["label"]
].copy()


# Insert OOF TF-IDF probability
fusion_df.insert(
    1,
    "tfidf_attack_probability",
    oof_probability
)


# ============================================================
# FINAL CHECK
# ============================================================

print("\n" + "=" * 80)
print("RISK FUSION DATASET")
print("=" * 80)

print(
    f"Samples : {len(fusion_df)}"
)

print(
    f"Columns : {len(fusion_df.columns)}"
)

print(
    f"Shape   : {fusion_df.shape}"
)

print("\nLabel Distribution:")
print(
    fusion_df["label"].value_counts()
)


print("\nMissing values:")
print(
    fusion_df.isnull().sum().sum()
)


# ============================================================
# SAVE
# ============================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

fusion_df.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nSaved to:")
print(OUTPUT_PATH)