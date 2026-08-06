from gateway.core.config import settings
from gateway.models.risk import RiskReport
from gateway.models.threat import ThreatReport


class RiskAdapter:

    def assess(self, report: ThreatReport) -> RiskReport:

        if settings.INTEGRATION_MODE == "local":
            return self._local(report)

        return self._remote(report)

    def _local(self, report: ThreatReport) -> RiskReport:

        if report.attack_probability > 0.8:
            return RiskReport(
                risk_score=95,
                risk_level="Critical",
                action="BLOCK",
                confidence=0.98,
            )

        return RiskReport(
            risk_score=18,
            risk_level="Low",
            action="ALLOW",
            confidence=0.95,
        )

    def _remote(self, report: ThreatReport) -> RiskReport:

        raise NotImplementedError(
            "Remote Risk Engine integration not implemented yet."
        )