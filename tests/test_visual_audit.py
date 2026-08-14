
import pytest
from pathlib import Path
from app.services.providers.null_vlm import NullVLMProvider
from app.models.audit import BrowserAuditResult, ElementBounds
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
    
def test_visual_audit_service_prepares_input_from_browser_result() -> None:
    browser_result = BrowserAuditResult(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=Path("artifacts/test.png"),
        dom_snapshot="<html><body></body></html>",
        element_bounds={
            "h1": ElementBounds(
                x=10,
                y=20,
                width=100,
                height=30,
            )
        },
    )

    service = VisualAuditService(None)

    visual_input = service.prepare_input(browser_result)

    assert visual_input.job_id == browser_result.job_id
    assert visual_input.target_url == browser_result.target_url
    assert visual_input.viewport == browser_result.viewport
    assert visual_input.screenshot_path == str(browser_result.screenshot_path)
    assert visual_input.dom_snapshot == browser_result.dom_snapshot
    assert visual_input.element_bounds == browser_result.element_bounds
    
@pytest.mark.asyncio
async def test_visual_audit_service_works_with_null_provider() -> None:
    audit_input = VisualAuditInput(
        job_id="test-job",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path="artifacts/test.png",
        dom_snapshot="<html></html>",
    )

    service = VisualAuditService(NullVLMProvider())

    result = await service.audit(audit_input)

    assert result.job_id == "test-job"
    assert result.target_url == "https://example.com"
    assert result.viewport == "desktop"
    assert result.defect_count == 0