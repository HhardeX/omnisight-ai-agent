from dataclasses import dataclass
from pathlib import Path

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

    def apply_css_fix(
        self,
        output_path: str | Path,
        fix: ProposedFix,
    ) -> Path:
        """Write a proposed CSS fix to an isolated patch file."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        selector = fix.element_selector.strip()
        suggested_css = fix.suggested_css.strip()

        if not selector:
            raise ValueError("CSS fix selector cannot be empty.")

        if not suggested_css:
            raise ValueError("CSS fix declarations cannot be empty.")

        css_rule = (
            f"{selector} {{\n"
            f"    {suggested_css}\n"
            f"}}\n"
        )

        path.write_text(
            css_rule,
            encoding="utf-8",
        )

        return path
