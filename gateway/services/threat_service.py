from gateway.adapters.threat_adapter import ThreatAdapter
from gateway.models.threat import ThreatReport


class ThreatService:

    def analyze(self, prompt: str) -> ThreatReport:
        """
        Placeholder for Person 1 Threat Intelligence Engine.
        """

        return ThreatReport(
            linguistic={},
            structural={},
            semantic={},
            attack_probability=0.15,
            confidence=0.96
        )





class ThreatService:

    def __init__(self):
        self.adapter = ThreatAdapter()

    def analyze(self, prompt: str):
        return self.adapter.analyze(prompt)