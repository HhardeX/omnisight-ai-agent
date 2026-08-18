from pathlib import Path

from app.models.visual import (
    VisualAuditInput,
    VisualAuditResponse,
    VisualDefect,
)
from app.services.vlm import VLMProvider


class RuleBasedVLMProvider(VLMProvider):
    """Deterministic visual-audit provider used as a VLM integration baseline."""

    async def analyze(
        self,
        audit_input: VisualAuditInput,
    ) -> VisualAuditResponse:
        screenshot = Path(audit_input.screenshot_path)

        if not screenshot.is_file():
            raise FileNotFoundError(
                f"Screenshot not found: {screenshot}"
            )

        defects: list[VisualDefect] = []

        if not audit_input.dom_snapshot.strip():
            defects.append(
                VisualDefect(
                    element_selector="html",
                    defect_type="missing_dom",
                    description="The captured page contains no DOM content.",
                    suggested_css=None,
                    confidence_score=1.0,
                    bounding_box=None,
                )
            )

        if (
            audit_input.dom_snapshot.strip()
            and "<h1" not in audit_input.dom_snapshot.lower()
        ):
            defects.append(
                VisualDefect(
                    element_selector="h1",
                    defect_type="missing_h1",
                    description="The captured page does not contain a primary heading.",
                    suggested_css=None,
                    confidence_score=0.95,
                    bounding_box=None,
                )
            )

        return VisualAuditResponse(
            job_id=audit_input.job_id,
            target_url=audit_input.target_url,
            viewport=audit_input.viewport,
            defects=defects,
        )