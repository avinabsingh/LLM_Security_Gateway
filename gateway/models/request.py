from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Prompt submitted by the user."
    )