from pydantic import BaseModel, Field

from app.models.audit import ElementBounds


class VisualAuditInput(BaseModel):
    """Structured browser data provided to the visual-audit stage."""

    job_id: str = Field(min_length=1)
    target_url: str = Field(min_length=1)
    viewport: str = Field(min_length=1)

    screenshot_path: str = Field(min_length=1)
    dom_snapshot: str
    element_bounds: dict[str, ElementBounds] = Field(default_factory=dict)

class VisualDefect(BaseModel):
    """Structured representation of a detected visual defect."""

    element_selector: str = Field(min_length=1)
    defect_type: str = Field(min_length=1)
    description: str = Field(min_length=1)

    suggested_css: str | None = None

    confidence_score: float = Field(ge=0.0, le=1.0)

    bounding_box: ElementBounds | None = None

class VisualAuditResponse(BaseModel):
    """Structured result produced by the visual-audit stage."""

    job_id: str = Field(min_length=1)
    target_url: str = Field(min_length=1)
    viewport: str = Field(min_length=1)

    defects: list[VisualDefect] = Field(default_factory=list)

    @property
    def defect_count(self) -> int:
        """Return the number of detected visual defects."""
        return len(self.defects)

