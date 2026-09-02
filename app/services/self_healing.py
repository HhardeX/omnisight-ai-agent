from dataclasses import dataclass

from app.models.visual import VisualAuditResponse


@dataclass(frozen=True)
class ProposedFix:
    """A validated CSS fix proposed for a detected visual defect."""

    element_selector: str
    suggested_css: str


class SelfHealingService:
    """Prepare safe, deterministic fixes from visual audit results."""

    def collect_fixes(
        self,
        visual_result: VisualAuditResponse,
    ) -> list[ProposedFix]:
        """Return defects that contain usable CSS suggestions."""

        fixes: list[ProposedFix] = []

        for defect in visual_result.defects:
            if not defect.suggested_css:
                continue

            suggested_css = defect.suggested_css.strip()

            if not suggested_css:
                continue

            fixes.append(
                ProposedFix(
                    element_selector=defect.element_selector,
                    suggested_css=suggested_css,
                )
            )

        return fixes
