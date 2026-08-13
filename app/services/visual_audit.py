from app.models.visual import VisualAuditInput, VisualAuditResponse


from app.services.vlm import VLMProvider


class VisualAuditService:
    """Service boundary for visual UI auditing."""

    def __init__(self, provider: VLMProvider) -> None:
        self._provider = provider

    async def audit(self, audit_input: VisualAuditInput) -> VisualAuditResponse:
        """Run a visual audit using the configured VLM provider."""
        return await self._provider.analyze(audit_input)