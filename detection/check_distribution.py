import pandas as pd
from pathlib import Path

# ---------------------------------------
# Project Root & Paths
# ---------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TRAIN_PATH = BASE_DIR / "training" / "artifacts" / "hybrid_train_features.csv"
TEST_PATH = BASE_DIR / "training" / "artifacts" / "hybrid_test_features.csv"

def print_distribution(file_path, dataset_name):
    print(f"\n{'='*40}")
    print(f"{dataset_name.upper()} CLASS DISTRIBUTION")
    print(f"{'='*40}")
    
    try:
        df = pd.read_csv(file_path)
        
        # Raw counts
        counts = df['label'].value_counts()
        
        # Percentages
        percentages = df['label'].value_counts(normalize=True) * 100
        
        # Combine into a clean DataFrame for display
        distribution_df = pd.DataFrame({
            'Raw Count': counts,
            'Percentage': percentages.round(2).astype(str) + '%'
        })
        
        # Map 0 and 1 to human-readable labels if needed
        distribution_df.index = distribution_df.index.map({0: 'Safe (0)', 1: 'Attack (1)'})
        
        print(distribution_df)
        print("-" * 40)
        print(f"Total Samples: {len(df)}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {file_path.name}")

if __name__ == "__main__":
    print_distribution(TRAIN_PATH, "Training Data")
    print_distribution(TEST_PATH, "Testing Data")