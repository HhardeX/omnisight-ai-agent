
from pathlib import Path

import pytest

from app.models.audit import BrowserAuditResult, ElementBounds
from app.models.visual import VisualAuditResponse, VisualDefect
from app.services.self_healing import ProposedFix
from app.services.self_healing_workflow import SelfHealingWorkflow
from app.services.visual_audit import VisualAuditService
from app.services.vlm import VLMProvider


class FakeVLMProvider(VLMProvider):
    """Deterministic VLM provider used for verification testing."""

    async def analyze(
        self,
        audit_input,
    ) -> VisualAuditResponse:
        return VisualAuditResponse(
            job_id=audit_input.job_id,
            target_url=audit_input.target_url,
            viewport=audit_input.viewport,
            defects=[],
        )


class FakeBrowserManager:
    """Deterministic browser manager used for workflow testing."""

    def __init__(self) -> None:
        self.injected_css = None
        self.screenshot_path = None

    async def inject_css(self, css: str) -> None:
        self.injected_css = css

    async def screenshot(
        self,
        output_path: str,
        full_page: bool = True,
    ) -> Path:
        self.screenshot_path = output_path
        return Path(output_path)

    async def get_dom_snapshot(self) -> str:
        return "<html><body><h1>Healed</h1></body></html>"

    async def get_element_bounds(
        self,
        selector: str,
    ) -> dict[str, float] | None:
        if selector == "h1":
            return {
                "x": 10,
                "y": 20,
                "width": 200,
                "height": 40,
            }

        return None


def test_workflow_collects_fixes() -> None:
    visual_result = VisualAuditResponse(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        defects=[],
    )

    workflow = SelfHealingWorkflow()

    fixes = workflow.collect_fixes(visual_result)

    assert fixes == []


def test_workflow_applies_css_fix(tmp_path: Path) -> None:
    output_path = tmp_path / "healing-patch.css"

    fix = ProposedFix(
        element_selector="#login",
        suggested_css="margin-top: 8px;",
    )

    workflow = SelfHealingWorkflow()

    patch_path = workflow.apply_fix(
        str(output_path),
        fix,
    )

    assert patch_path == str(output_path)
    assert output_path.exists()


def test_workflow_verifies_clean_result() -> None:
    verification = VisualAuditResponse(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        defects=[],
    )

    assert SelfHealingWorkflow.is_verified(verification) is True


def test_workflow_rejects_result_with_defects() -> None:
    verification = VisualAuditResponse(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        defects=[
            VisualDefect(
                element_selector="#login",
                defect_type="spacing",
                description="Login button still has incorrect spacing.",
                suggested_css="margin-top: 8px;",
                confidence_score=0.95,
            ),
        ],
    )

    assert SelfHealingWorkflow.is_verified(verification) is False


@pytest.mark.asyncio
async def test_workflow_verifies_fix_with_vlm() -> None:
    browser_result = BrowserAuditResult(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=Path("artifacts/verification.png"),
        dom_snapshot="<html><body></body></html>",
    )

    visual_service = VisualAuditService(
        FakeVLMProvider()
    )

    workflow = SelfHealingWorkflow()

    verification = await workflow.verify_fix(
        browser_result,
        visual_service,
    )

    assert verification.job_id == "job-1"
    assert verification.target_url == "https://example.com"
    assert verification.viewport == "desktop"
    assert verification.defect_count == 0
    assert SelfHealingWorkflow.is_verified(verification) is True


@pytest.mark.asyncio
async def test_workflow_injects_generated_fix(
    tmp_path: Path,
) -> None:
    workflow = SelfHealingWorkflow()
    browser_manager = FakeBrowserManager()

    patch_path = tmp_path / "healing-patch.css"

    patch_path.write_text(
        "#login {\n"
        "    margin-top: 8px;\n"
        "}\n",
        encoding="utf-8",
    )

    await workflow.inject_fix(
        browser_manager,
        str(patch_path),
    )

    assert browser_manager.injected_css == (
        "#login {\n"
        "    margin-top: 8px;\n"
        "}\n"
    )


@pytest.mark.asyncio
async def test_workflow_captures_post_fix_result(
    tmp_path: Path,
) -> None:
    workflow = SelfHealingWorkflow()
    browser_manager = FakeBrowserManager()

    screenshot_path = tmp_path / "post-fix.png"

    result = await workflow.capture_post_fix_result(
        browser_manager=browser_manager,
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=str(screenshot_path),
    )

    assert result.job_id == "job-1"
    assert result.target_url == "https://example.com"
    assert result.viewport == "desktop"
    assert result.screenshot_path == screenshot_path
    assert result.dom_snapshot == (
        "<html><body><h1>Healed</h1></body></html>"
    )

    assert result.element_bounds["h1"] == ElementBounds(
        x=10,
        y=20,
        width=200,
        height=40,
    )


@pytest.mark.asyncio
async def test_workflow_heals_and_verifies_fix(
    tmp_path: Path,
) -> None:
    workflow = SelfHealingWorkflow()
    browser_manager = FakeBrowserManager()

    visual_result = VisualAuditResponse(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        defects=[
            VisualDefect(
                element_selector="#login",
                defect_type="spacing",
                description="Login button has incorrect spacing.",
                suggested_css="margin-top: 8px;",
                confidence_score=0.95,
            ),
        ],
    )

    visual_service = VisualAuditService(
        FakeVLMProvider()
    )

    healing_directory = tmp_path / "healing"

    attempts = await workflow.heal(
        browser_manager=browser_manager,
        visual_result=visual_result,
        visual_service=visual_service,
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        patch_directory=str(healing_directory),
    )

    assert len(attempts) == 1

    attempt = attempts[0]

    assert attempt.fix.element_selector == "#login"
    assert attempt.fix.suggested_css == "margin-top: 8px;"

    assert Path(attempt.patch_path).exists()

    assert browser_manager.injected_css == (
        "#login {\n"
        "    margin-top: 8px;\n"
        "}\n"
    )

    assert attempt.verification.defect_count == 0
    assert workflow.is_verified(attempt.verification) is True
