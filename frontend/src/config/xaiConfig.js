export const featureDictionary = {
    baseline_attack_probability: {
        label: "Deep Learning Intent",
        category: "AI Model",
        color: "bg-purple-100 text-purple-800",
        description: "The DeBERTa neural network's assessment of malicious semantic intent."
    },
    attack_similarity: {
        label: "Semantic Match",
        category: "Embeddings",
        color: "bg-blue-100 text-blue-800",
        description: "Measures mathematical similarity to known jailbreak prompts in our vector database."
    },
    prompt_leakage: {
        label: "System Prompt Extraction",
        category: "Structural",
        color: "bg-orange-100 text-orange-800",
        description: "Explicit commands attempting to force the AI to reveal its core instructions."
    },
    char_length: {
        label: "Character Count",
        category: "Heuristic",
        color: "bg-gray-100 text-gray-800",
        description: "The total length of the prompt. Abnormally long prompts often indicate context-stuffing attacks."
    },
    word_count: {
        label: "Word Count",
        category: "Heuristic",
        color: "bg-gray-100 text-gray-800",
        description: "Total words. Extreme lengths can be used to obfuscate malicious commands."
    },
    special_characters: {
        label: "Special Character Density",
        category: "Obfuscation",
        color: "bg-red-100 text-red-800",
        description: "High counts of symbols often indicate encoding or formatting attacks."
    },
    unicode_anomaly: {
        label: "Unicode Anomaly",
        category: "Obfuscation",
        color: "bg-red-100 text-red-800",
        description: "Detects hidden or non-standard characters used to bypass simple text filters."
    },
    uppercase_letters: {
        label: "Uppercase Density",
        category: "Heuristic",
        color: "bg-gray-100 text-gray-800",
        description: "Excessive capitalization, sometimes used in adversarial formatting."
    }
};