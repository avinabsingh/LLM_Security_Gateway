from gateway.models.risk import RiskReport
from gateway.services.risk_service import RiskService
from gateway.services.threat_service import ThreatService


class GatewayService:

    def __init__(self):
        self.threat_service = ThreatService()
        self.risk_service = RiskService()

    def analyze(self, prompt: str) -> RiskReport:

        threat_report = self.threat_service.analyze(prompt)

        risk_report = self.risk_service.assess(threat_report)

        return risk_report