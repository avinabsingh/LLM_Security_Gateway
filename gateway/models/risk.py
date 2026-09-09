from pydantic import BaseModel
from typing import List

class RiskFactor(BaseModel):
    feature: str
    value: float
    scaled: float
    coefficient: float
    contribution: float

class RiskReport(BaseModel):
    risk_score: float
    risk_level: str
    decision: str
    decision_reason: str
    top_risk_factors: List[RiskFactor]