import pandas as pd
from datasets import load_dataset

from pathlib import Path


class AlpacaAdapter:

    def __init__(self):

        self.dataset = None

        self.df = None

    def load(self):

        self.dataset = load_dataset(
            "yahma/alpaca-cleaned"
        )

        print("Dataset Loaded")

    def convert(self):

        rows = []

        for idx, sample in enumerate(self.dataset["train"]):

            rows.append({

                "id": idx,

                "prompt": sample["instruction"],

                "safe": 1,

                "prompt_injection": 0,

                "jailbreak": 0,

                "prompt_leakage": 0,

                "data_exfiltration": 0,

                "tool_abuse": 0,

                "context_manipulation": 0,

                "obfuscation": 0,

                "social_engineering": 0,

                "source_dataset": "alpaca"

            })

        self.df = pd.DataFrame(rows)

        print(self.df.head())

    def save(self):

        output = Path("../datasets/processed/unified_alpaca.csv")

        self.df.to_csv(output, index=False)

        print("Saved")


if __name__ == "__main__":

    adapter = AlpacaAdapter()

    adapter.load()

    adapter.convert()

    adapter.save()