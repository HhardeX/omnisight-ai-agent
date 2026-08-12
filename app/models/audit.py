from pathlib import Path

from pydantic import BaseModel, Field


class ElementBounds(BaseModel):
    """Bounding-box geometry for a DOM element."""

    x: float
    y: float
    width: float
    height: float


class BrowserAuditResult(BaseModel):
    """Structured result produced by the browser audit stage."""

    job_id: str = Field(min_length=1)
    target_url: str = Field(min_length=1)
    viewport: str = Field(min_length=1)

    screenshot_path: Path
    dom_snapshot: str
    element_bounds: dict[str, ElementBounds] = Field(default_factory=dict)

    @property
    def dom_size(self) -> int:
        """Return the number of characters in the captured DOM."""
        return len(self.dom_snapshot)