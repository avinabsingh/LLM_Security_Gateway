from gateway.models.risk import RiskReport
from gateway.models.threat import ThreatReport


class RiskService:

    def assess(self, report: ThreatReport) -> RiskReport:
        """
        Placeholder for Person 2 Risk Assessment Engine.
        """

        if report.attack_probability > 0.8:
            return RiskReport(
                risk_score=95,
                risk_level="Critical",
                action="BLOCK",
                confidence=0.97
            )

        return RiskReport(
            risk_score=20,
            risk_level="Low",
            action="ALLOW",
            confidence=0.94
        )