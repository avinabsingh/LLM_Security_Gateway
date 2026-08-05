class StructuralFeatures:

    PATTERNS = {

        "instruction_override": [
            "ignore previous instructions",
            "ignore all previous instructions",
            "ignore earlier instructions",
            "disregard previous instructions",
            "disregard all previous instructions",
            "forget previous instructions",
            "forget all instructions"
        ],

        "memory_reset": [
            "forget everything",
            "forget previous conversation",
            "reset your memory",
            "clear your memory",
            "start from scratch"
        ],

        "developer_mode": [
            "developer mode",
            "enable developer mode",
            "activate developer mode"
        ],

        "prompt_leakage": [
            "system prompt",
            "hidden instructions",
            "internal instructions",
            "initial instructions",
            "secret instructions"
        ],

        "information_extraction": [
            "reveal",
            "show me",
            "print",
            "display",
            "give me your instructions"
        ],

        "jailbreak": [
            "dan",
            "do anything now",
            "no restrictions",
            "without restrictions",
            "bypass safety",
            "ignore safety",
            "remove restrictions"
        ],

        "role_change": [
            "pretend you are",
            "act as",
            "roleplay as",
            "you are now",
            "behave as"
        ],

        "encoding": [
            "base64",
            "unicode",
            "hex encoded",
            "hexadecimal",
            "rot13"
        ],

        "authority_claim": [
            "i am your developer",
            "i am the administrator",
            "admin approved",
            "developer approved",
            "authorized by the administrator"
        ],

        "urgency_manipulation": [
            "this is an emergency",
            "urgent override",
            "emergency override",
            "immediately bypass"
        ]
    }


    def extract(self, prompt: str):

        prompt_lower = prompt.lower()

        features = {}

        for signal, patterns in self.PATTERNS.items():

            matched_patterns = [
                pattern
                for pattern in patterns
                if pattern in prompt_lower
            ]

            features[signal] = int(
                len(matched_patterns) > 0
            )

        return features