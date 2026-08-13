from gateway.adapters.risk_adapter import RiskAdapter
from gateway.models.risk import RiskReport
from gateway.models.threat import ThreatReport


class RiskService:

    def __init__(self):
        self.adapter = RiskAdapter()

    def assess(self, report: ThreatReport) -> RiskReport:
        return self.adapter.assess(report)