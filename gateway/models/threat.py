from pydantic import BaseModel


class ThreatReport(BaseModel):

    prompt: str

    linguistic: dict

    structural: dict

    semantic: dict

    attack_probability: float

    confidence: float