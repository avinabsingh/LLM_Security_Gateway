import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "evaluation"
    / "fusion"
    / "risk_fusion_test.csv"
)


print("=" * 80)
print("FALSE NEGATIVE RECOVERY ANALYSIS")
print("=" * 80)

df = pd.read_csv(DATA_PATH)


# --------------------------------------------------
# Baseline
# --------------------------------------------------

df["baseline_prediction"] = (
    df["tfidf_attack_probability"] >= 0.5
).astype(int)


fn = df[
    (df["label"] == 1) &
    (df["baseline_prediction"] == 0)
].copy()


print(f"\nFalse negatives: {len(fn)}")


# --------------------------------------------------
# Recovery Rules
# --------------------------------------------------

fn["obfuscation_recovery"] = (
    fn["obfuscation_score"] >= 0.10
)

fn["strong_obfuscation"] = (
    fn["obfuscation_score"] >= 0.25
)

fn["semantic_recovery"] = (
    fn["attack_similarity"] >= 0.25
)

fn["strong_semantic"] = (
    fn["attack_similarity"] >= 0.30
)


structural_columns = [
    "instruction_override",
    "memory_reset",
    "developer_mode",
    "prompt_leakage",
    "information_extraction",
    "jailbreak",
    "role_change",
    "encoding",
    "authority_claim",
    "urgency_manipulation"
]


fn["structural_recovery"] = (
    fn[structural_columns].sum(axis=1) > 0
)


# --------------------------------------------------
# Individual Recovery
# --------------------------------------------------

print("\n" + "=" * 80)
print("INDIVIDUAL SIGNAL RECOVERY")
print("=" * 80)

print(
    f"Obfuscation >= 0.10 : "
    f"{fn['obfuscation_recovery'].sum()}"
)

print(
    f"Obfuscation >= 0.25 : "
    f"{fn['strong_obfuscation'].sum()}"
)

print(
    f"Semantic >= 0.25    : "
    f"{fn['semantic_recovery'].sum()}"
)

print(
    f"Semantic >= 0.30    : "
    f"{fn['strong_semantic'].sum()}"
)

print(
    f"Structural signal   : "
    f"{fn['structural_recovery'].sum()}"
)


# --------------------------------------------------
# Combined Recovery
# --------------------------------------------------

fn["recoverable"] = (
    fn["obfuscation_recovery"]
    |
    fn["semantic_recovery"]
    |
    fn["structural_recovery"]
)


print("\n" + "=" * 80)
print("COMBINED RECOVERY")
print("=" * 80)

print(
    f"Recoverable FNs: "
    f"{fn['recoverable'].sum()} / {len(fn)}"
)

print(
    f"Recovery rate: "
    f"{fn['recoverable'].mean():.4f}"
)


# --------------------------------------------------
# Strong Combined Rule
# --------------------------------------------------

fn["strong_recoverable"] = (
    (
        fn["obfuscation_score"] >= 0.10
    )
    &
    (
        fn["attack_similarity"] >= 0.15
    )
) | (
    fn["structural_recovery"]
)


print("\n" + "=" * 80)
print("COMBINED SECURITY SIGNAL")
print("=" * 80)

print(
    f"Strong recoverable: "
    f"{fn['strong_recoverable'].sum()} / {len(fn)}"
)


# --------------------------------------------------
# Print Recoverable Samples
# --------------------------------------------------

print("\n" + "=" * 80)
print("RECOVERABLE FALSE NEGATIVES")
print("=" * 80)


for i, (_, row) in enumerate(
    fn[fn["recoverable"]].iterrows(),
    start=1
):

    print("\n" + "-" * 80)

    print(
        f"#{i}"
    )

    print(
        f"TF-IDF       : "
        f"{row['tfidf_attack_probability']:.4f}"
    )

    print(
        f"Semantic     : "
        f"{row['attack_similarity']:.4f}"
    )

    print(
        f"Obfuscation  : "
        f"{row['obfuscation_score']:.4f}"
    )

    print(
        f"Structural   : "
        f"{int(row['structural_recovery'])}"
    )

    print(
        f"Prompt: {str(row['prompt'])[:500]}"
    )