from pathlib import Path

# Root directory
ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = ROOT / "raw"

DATASETS = [
    "prompt_injection",
    "jailbreak",
    "benign",
    "rag",
    "obfuscation"
]

def create_directories():
    """
    Create all dataset folders if they do not exist.
    """

    for folder in DATASETS:
        path = RAW_DATA / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] {path}")

if __name__ == "__main__":
    create_directories()