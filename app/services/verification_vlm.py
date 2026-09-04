from abc import ABC, abstractmethod
from pathlib import Path

from app.models.visual import VisualDefect
from app.models.verification import VisualVerificationResult


class VerificationVLMProvider(ABC):
    """Provider-agnostic interface for visual fix verification."""

    @abstractmethod
    async def verify(
        self,
        job_id: str,
        target_url: str,
        viewport: str,
        before_screenshot: Path,
        after_screenshot: Path,
        defect: VisualDefect,
    ) -> VisualVerificationResult:
        """Verify whether a visual defect was fixed."""
        raise NotImplementedError