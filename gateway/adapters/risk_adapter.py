import sys

from gateway.core.config import settings
from gateway.models.risk import RiskReport
from gateway.models.threat import ThreatReport


sys.path.insert(0, "detection")

from inference.risk_fusion_engine import RiskFusionEngine


class RiskAdapter:

    def __init__(self):
        self.engine = RiskFusionEngine(threshold=0.92)

    def assess(self, report: ThreatReport) -> RiskReport:

        if settings.INTEGRATION_MODE == "local":
            return self._local(report)

        return self._remote(report)

    def _local(self, report: ThreatReport) -> RiskReport:

        result = self.engine.analyze(report.prompt)

        return RiskReport(
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            decision=result["decision"],
            decision_reason=result["decision_reason"],
            top_risk_factors=result["top_risk_factors"],
        )

    def _remote(self, report: ThreatReport) -> RiskReport:

        raise NotImplementedError(
            "Remote Risk Engine integration not implemented yet."
        )