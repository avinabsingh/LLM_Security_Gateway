from features.linguistic import LinguisticFeatures
from features.structural import StructuralFeatures
from features.semantic import SemanticFeatures
from features.obfuscation import ObfuscationDetector

class ThreatFeatureExtractor:

    def __init__(self):

        print("Initializing Threat Feature Extractor...")

        self.linguistic = LinguisticFeatures()
        self.structural = StructuralFeatures()

        # Heavy model — load only once
        self.semantic = SemanticFeatures()

        self.obfuscation = ObfuscationDetector()

        print("Threat Feature Extractor Ready")


    def extract(self, prompt: str):

        linguistic_features = self.linguistic.extract(prompt)

        structural_features = self.structural.extract(prompt)

        semantic_result = self.semantic.attack_similarity(
            prompt,
            top_k=3
        )

        obfuscation = self.obfuscation.analyze(prompt)

        report = {

            "prompt": prompt,

            "linguistic": linguistic_features,

            "structural": structural_features,

            "semantic": {
                "attack_similarity": semantic_result["top_score"],
                "nearest_attack": semantic_result["nearest_attack"],
                "top_matches": semantic_result["matches"]
            },

            "obfuscation": obfuscation
        }

        return report