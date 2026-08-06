from pydantic import BaseModel


class RiskReport(BaseModel):

    risk_score: float

    risk_level: str

    action: str

    confidence: float