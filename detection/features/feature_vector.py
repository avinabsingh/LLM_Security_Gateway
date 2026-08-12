class FeatureVectorBuilder:

    def __init__(self):

        self.feature_names = [

            # -----------------------------
            # Linguistic
            # -----------------------------

            "char_length",
            "word_count",
            "question_marks",
            "exclamation_marks",
            "uppercase_letters",
            "digits",
            "special_characters",

            # -----------------------------
            # Structural
            # -----------------------------

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

            # -----------------------------
            # Semantic
            # -----------------------------

            "attack_similarity",

            # -----------------------------
            # Obfuscation
            # -----------------------------

            "unicode_anomaly",
            "leetspeak",
            "symbol_substitution",
            "base64",
            "binary",
            "hexadecimal",
            "obfuscation_score"
        ]


    def build(self, report):

        linguistic = report["linguistic"]

        structural = report["structural"]

        semantic = report["semantic"]

        obfuscation = report["obfuscation"]


        vector = [

            # Linguistic

            linguistic["char_length"],
            linguistic["word_count"],
            linguistic["question_marks"],
            linguistic["exclamation_marks"],
            linguistic["uppercase_letters"],
            linguistic["digits"],
            linguistic["special_characters"],


            # Structural

            structural["instruction_override"],
            structural["memory_reset"],
            structural["developer_mode"],
            structural["prompt_leakage"],
            structural["information_extraction"],
            structural["jailbreak"],
            structural["role_change"],
            structural["encoding"],
            structural["authority_claim"],
            structural["urgency_manipulation"],


            # Semantic

            semantic["attack_similarity"],


            # Obfuscation

            obfuscation["unicode_anomaly"],
            obfuscation["leetspeak"],
            obfuscation["symbol_substitution"],
            obfuscation["base64"],
            obfuscation["binary"],
            obfuscation["hexadecimal"],
            obfuscation["obfuscation_score"]
        ]


        return vector


    def get_feature_names(self):

        return self.feature_names