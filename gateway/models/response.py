from pydantic import BaseModel

from gateway.models.risk import RiskReport


class AnalyzeResponse(BaseModel):

    status: str

    risk: RiskReport