from pydantic import BaseModel


class ThreatReport(BaseModel):

    linguistic: dict

    structural: dict

    semantic: dict

    attack_probability: float

    confidence: float