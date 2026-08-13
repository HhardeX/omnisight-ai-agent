
import pytest
from app.models.visual import VisualAuditInput, VisualAuditResponse
from app.services.visual_audit import VisualAuditService
from app.services.vlm import VLMProvider


class FakeVLMProvider(VLMProvider):
    """Deterministic VLM provider used for service testing."""

    async def analyze(
        self,
        audit_input: VisualAuditInput,
    ) -> VisualAuditResponse:
        return VisualAuditResponse(
            job_id=audit_input.job_id,
            target_url=audit_input.target_url,
            viewport=audit_input.viewport,
        )

@pytest.mark.asyncio
async def test_visual_audit_service_delegates_to_provider() -> None:
    audit_input = VisualAuditInput(
        job_id="test-job",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path="artifacts/test.png",
        dom_snapshot="<html></html>",
    )

    service = VisualAuditService(FakeVLMProvider())

    result = await service.audit(audit_input)

    assert result.job_id == "test-job"
    assert result.target_url == "https://example.com"
    assert result.viewport == "desktop"
    assert result.defect_count == 0