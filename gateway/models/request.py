from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    prompt: str

class MultiTurnRequest(BaseModel):
    prompt: str
    session_id: str