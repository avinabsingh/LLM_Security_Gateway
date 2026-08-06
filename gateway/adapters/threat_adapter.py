from gateway.core.config import settings
from gateway.models.threat import ThreatReport


class ThreatAdapter:

    def analyze(self, prompt: str) -> ThreatReport:

        if settings.INTEGRATION_MODE == "local":
            return self._local(prompt)

        return self._remote(prompt)

    def _local(self, prompt: str) -> ThreatReport:
        """
        Local integration.
        Person 1's engine will be imported here later.
        """

        return ThreatReport(
            linguistic={},
            structural={},
            semantic={},
            attack_probability=0.15,
            confidence=0.96,
        )

    def _remote(self, prompt: str) -> ThreatReport:
        """
        HTTP integration.
        Will call Person 1's FastAPI service later.
        """

        raise NotImplementedError(
            "Remote Threat Engine integration not implemented yet."
        )