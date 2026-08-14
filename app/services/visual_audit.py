from app.models.audit import BrowserAuditResult
from app.models.visual import VisualAuditInput, VisualAuditResponse
from app.services.vlm import VLMProvider


class VisualAuditService:
    """Service boundary for visual UI auditing."""

    def __init__(self, provider: VLMProvider) -> None:
        self._provider = provider

    def prepare_input(
        self,
        browser_result: BrowserAuditResult,
    ) -> VisualAuditInput:
        """Convert browser audit output into visual-audit input."""
        return VisualAuditInput(
            job_id=browser_result.job_id,
            target_url=browser_result.target_url,
            viewport=browser_result.viewport,
            screenshot_path=str(browser_result.screenshot_path),
            dom_snapshot=browser_result.dom_snapshot,
            element_bounds=browser_result.element_bounds,
        )

    async def audit(self, audit_input: VisualAuditInput) -> VisualAuditResponse:
        """Run a visual audit using the configured VLM provider."""
        return await self._provider.analyze(audit_input)