from dataclasses import dataclass
from pathlib import Path

from app.browser.navigator import BrowserManager
from app.models.audit import BrowserAuditResult, ElementBounds
from app.models.visual import VisualAuditResponse
from app.services.self_healing import ProposedFix, SelfHealingService
from app.services.visual_audit import VisualAuditService


@dataclass(frozen=True)
class HealingAttempt:
    """Result of one self-healing attempt."""

    fix: ProposedFix
    patch_path: str
    verification: VisualAuditResponse


class SelfHealingWorkflow:
    """Coordinate fix preparation and post-fix verification."""

    def __init__(
        self,
        healing_service: SelfHealingService | None = None,
    ) -> None:
        self._healing_service = (
            healing_service or SelfHealingService()
        )

    def collect_fixes(
        self,
        visual_result: VisualAuditResponse,
    ) -> list[ProposedFix]:
        """Collect usable fixes from a visual audit result."""

        return self._healing_service.collect_fixes(
            visual_result
        )

    def apply_fix(
        self,
        output_path: str,
        fix: ProposedFix,
    ) -> str:
        """Generate an isolated CSS patch for a proposed fix."""

        path = self._healing_service.apply_css_fix(
            output_path,
            fix,
        )

        return str(path)

    async def inject_fix(
        self,
        browser_manager: BrowserManager,
        patch_path: str,
    ) -> None:
        """Inject a generated CSS patch into the active browser page."""

        css = Path(patch_path).read_text(
            encoding="utf-8"
        )

        await browser_manager.inject_css(css)

    async def capture_post_fix_result(
        self,
        browser_manager: BrowserManager,
        job_id: str,
        target_url: str,
        viewport: str,
        screenshot_path: str,
    ) -> BrowserAuditResult:
        """Capture the browser state after a healing fix."""

        screenshot = await browser_manager.screenshot(
            screenshot_path,
            full_page=True,
        )

        dom_snapshot = await browser_manager.get_dom_snapshot()

        element_bounds: dict[str, ElementBounds] = {}

        h1_bounds = await browser_manager.get_element_bounds(
            "h1"
        )

        if h1_bounds is not None:
            element_bounds["h1"] = ElementBounds(
                **h1_bounds
            )

        return BrowserAuditResult(
            job_id=job_id,
            target_url=target_url,
            viewport=viewport,
            screenshot_path=screenshot,
            dom_snapshot=dom_snapshot,
            element_bounds=element_bounds,
        )

    async def verify_fix(
        self,
        browser_result: BrowserAuditResult,
        visual_service: VisualAuditService,
    ) -> VisualAuditResponse:
        """Run a VLM audit against a post-fix browser capture."""

        visual_input = visual_service.prepare_input(
            browser_result
        )

        return await visual_service.audit(
            visual_input
        )

    async def heal(
        self,
        browser_manager: BrowserManager,
        visual_result: VisualAuditResponse,
        visual_service: VisualAuditService,
        job_id: str,
        target_url: str,
        viewport: str,
        patch_directory: str = "artifacts/healing",
    ) -> list[HealingAttempt]:
        """Apply available fixes and verify each fix with the VLM."""

        fixes = self.collect_fixes(visual_result)

        if not fixes:
            return []

        attempts: list[HealingAttempt] = []

        for index, fix in enumerate(fixes, start=1):
            patch_path = Path(patch_directory) / (
                f"{job_id}-{viewport}-fix-{index}.css"
            )

            patch_path_string = self.apply_fix(
                str(patch_path),
                fix,
            )

            await self.inject_fix(
                browser_manager,
                patch_path_string,
            )

            post_fix_screenshot = (
                Path("artifacts")
                / f"{job_id}-{viewport}-post-fix-{index}.png"
            )

            post_fix_result = (
                await self.capture_post_fix_result(
                    browser_manager=browser_manager,
                    job_id=job_id,
                    target_url=target_url,
                    viewport=viewport,
                    screenshot_path=str(
                        post_fix_screenshot
                    ),
                )
            )

            verification = await self.verify_fix(
                post_fix_result,
                visual_service,
            )

            attempts.append(
                HealingAttempt(
                    fix=fix,
                    patch_path=patch_path_string,
                    verification=verification,
                )
            )

            if self.is_verified(verification):
                break

        return attempts

    @staticmethod
    def is_verified(
        verification: VisualAuditResponse,
    ) -> bool:
        """Return whether the verification audit found no defects."""

        return verification.defect_count == 0