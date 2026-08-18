from abc import ABC, abstractmethod

from app.models.visual import VisualAuditInput, VisualAuditResponse


class VLMProvider(ABC):
    """Provider-agnostic interface for visual UI analysis."""

    @abstractmethod
    async def analyze(
        self,
        audit_input: VisualAuditInput,
    ) -> VisualAuditResponse:
        """Analyze a browser capture and return structured visual findings."""
        raise NotImplementedError