from pydantic import BaseModel, Field


class VisualVerificationResult(BaseModel):
    """Structured result produced after verifying a UI fix."""

    job_id: str = Field(min_length=1)
    target_url: str = Field(min_length=1)
    viewport: str = Field(min_length=1)

    fixed: bool
    confidence_score: float = Field(ge=0.0, le=1.0)
    explanation: str = Field(min_length=1)