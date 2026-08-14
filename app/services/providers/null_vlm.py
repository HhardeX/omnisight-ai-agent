from app.models.visual import VisualAuditInput, VisualAuditResponse
from app.services.vlm import VLMProvider


class NullVLMProvider(VLMProvider):
    """Deterministic VLM provider used when no real VLM is configured."""

    async def analyze(
        self,
        audit_input: VisualAuditInput,
    ) -> VisualAuditResponse:
        return VisualAuditResponse(
            job_id=audit_input.job_id,
            target_url=audit_input.target_url,
            viewport=audit_input.viewport,
        )