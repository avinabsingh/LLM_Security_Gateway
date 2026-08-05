"""
Dataset Registry

Stores metadata for every dataset used in the project.
"""

DATASETS = {

    "promptbench": {
        "type": "huggingface",
        "dataset": "promptbench/PromptBench",
        "category": "prompt_injection"
    },

    "jailbreakbench": {
        "type": "huggingface",
        "dataset": "JailbreakBench/JBB-Behaviors",
        "category": "jailbreak"
    },

    "alpaca": {
        "type": "huggingface",
        "dataset": "yahma/alpaca-cleaned",
        "category": "benign"
    }

}