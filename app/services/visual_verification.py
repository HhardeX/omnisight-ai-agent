from pathlib import Path

from app.models.visual import VisualDefect
from app.models.verification import VisualVerificationResult
from app.services.verification_vlm import VerificationVLMProvider


class VisualVerificationService:
    """Service boundary for verifying visual fixes."""

    def __init__(self, provider: VerificationVLMProvider) -> None:
        self._provider = provider

    async def verify(
        self,
        job_id: str,
        target_url: str,
        viewport: str,
        before_screenshot_path: str,
        after_screenshot_path: str,
        defect: VisualDefect,
    ) -> VisualVerificationResult:
        """Verify whether the original visual defect was fixed."""

        before_screenshot = Path(before_screenshot_path)
        after_screenshot = Path(after_screenshot_path)

        if not before_screenshot.is_file():
            raise FileNotFoundError(
                f"Before screenshot not found: {before_screenshot}"
            )

        if not after_screenshot.is_file():
            raise FileNotFoundError(
                f"After screenshot not found: {after_screenshot}"
            )

        return await self._provider.verify(
            job_id=job_id,
            target_url=target_url,
            viewport=viewport,
            before_screenshot=before_screenshot,
            after_screenshot=after_screenshot,
            defect=defect,
        )