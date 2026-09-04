from pathlib import Path

import pytest

from app.models.visual import VisualDefect
from app.models.verification import VisualVerificationResult
from app.services.visual_verification import VisualVerificationService
from app.services.verification_vlm import VerificationVLMProvider


class FakeVerificationVLMProvider(VerificationVLMProvider):
    async def verify(
        self,
        job_id: str,
        target_url: str,
        viewport: str,
        before_screenshot: Path,
        after_screenshot: Path,
        defect: VisualDefect,
    ) -> VisualVerificationResult:
        return VisualVerificationResult(
            job_id=job_id,
            target_url=target_url,
            viewport=viewport,
            fixed=True,
            confidence_score=0.95,
            explanation="The original layout defect is no longer visible.",
        )


@pytest.mark.asyncio
async def test_visual_verification_service_returns_result(tmp_path):
    before = tmp_path / "before.png"
    after = tmp_path / "after.png"

    before.write_bytes(b"before")
    after.write_bytes(b"after")

    defect = VisualDefect(
        element_selector="#submit-button",
        defect_type="visibility",
        description="Submit button is hidden.",
        suggested_css="display: block;",
        confidence_score=0.95,
    )

    service = VisualVerificationService(FakeVerificationVLMProvider())

    result = await service.verify(
        job_id="job-123",
        target_url="http://localhost:3000",
        viewport="1280x720",
        before_screenshot_path=str(before),
        after_screenshot_path=str(after),
        defect=defect,
    )

    assert result.fixed is True
    assert result.confidence_score == 0.95
    assert result.job_id == "job-123"