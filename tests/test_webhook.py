
import pytest
from fastapi import BackgroundTasks
from pathlib import Path

from app.api import webhook
from app.models.audit import BrowserAuditResult
from app.models.jobs import BuildEvent
from app.models.visual import VisualAuditResponse, VisualDefect


def make_build_event() -> BuildEvent:
    return BuildEvent(
        repository="HhardeX/omnisight-ai-agent",
        commit_sha="fb29e74",
        branch="feature/Aishwarya",
        target_url="https://example.com",
    )


@pytest.mark.asyncio
async def test_receive_build_event_accepts_valid_event(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_job_id = "test-job-id"

    monkeypatch.setattr(
        webhook,
        "uuid4",
        lambda: expected_job_id,
    )

    background_tasks = BackgroundTasks()

    response = await webhook.receive_build_event(
        make_build_event(),
        background_tasks,
    )

    assert response == {
        "job_id": expected_job_id,
        "status": "accepted",
        "message": (
            "Build event accepted and responsive "
            "audit scheduled."
        ),
    }

    assert len(background_tasks.tasks) == 1


@pytest.mark.asyncio
async def test_receive_build_event_schedules_run_audit_job(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected_job_id = "scheduled-job-id"
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        webhook,
        "uuid4",
        lambda: expected_job_id,
    )

    async def fake_run_audit_job(
        job_id: str,
        event: BuildEvent,
    ) -> None:
        captured["job_id"] = job_id
        captured["event"] = event

    monkeypatch.setattr(
        webhook,
        "run_audit_job",
        fake_run_audit_job,
    )

    background_tasks = BackgroundTasks()
    event = make_build_event()

    await webhook.receive_build_event(
        event,
        background_tasks,
    )

    assert len(background_tasks.tasks) == 1

    await background_tasks()

    assert captured["job_id"] == expected_job_id
    assert captured["event"] == event


@pytest.mark.asyncio
async def test_attempt_visual_repair_applies_css_and_reaudits() -> None:
    class FakeManager:
        def __init__(self) -> None:
            self.applied_css: list[str] = []
            self.screenshots: list[tuple[object, bool]] = []

        async def apply_css(self, css: str) -> None:
            self.applied_css.append(css)

        async def screenshot(
            self,
            output_path: object,
            full_page: bool = True,
        ) -> object:
            self.screenshots.append(
                (output_path, full_page)
            )
            return output_path

        async def get_dom_snapshot(self) -> str:
            return (
                "<html>"
                "<body>"
                "<h1>Example</h1>"
                "</body>"
                "</html>"
            )

    class FakeVisualService:
        def __init__(
            self,
            repaired_result: VisualAuditResponse,
        ) -> None:
            self.repaired_result = repaired_result
            self.prepare_inputs: list[object] = []
            self.audit_inputs: list[object] = []

        def prepare_input(
            self,
            audit_result: BrowserAuditResult,
        ) -> object:
            self.prepare_inputs.append(audit_result)
            return audit_result

        async def audit(
            self,
            audit_input: object,
        ) -> VisualAuditResponse:
            self.audit_inputs.append(audit_input)
            return self.repaired_result

    manager = FakeManager()

    repaired_result = VisualAuditResponse(
        job_id="repair-job",
        target_url="https://example.com",
        viewport="mobile",
        defects=[],
    )

    visual_service = FakeVisualService(
        repaired_result
    )

    audit_result = BrowserAuditResult(
        job_id="repair-job",
        target_url="https://example.com",
        viewport="mobile",
        screenshot_path="artifacts/repair-job-mobile.png",
        dom_snapshot=(
            "<html>"
            "<body>"
            "<h1>Example</h1>"
            "</body>"
            "</html>"
        ),
    )

    initial_result = VisualAuditResponse(
        job_id="repair-job",
        target_url="https://example.com",
        viewport="mobile",
        defects=[
            VisualDefect(
                element_selector="h1",
                defect_type="unreadable text",
                description="Heading is difficult to read.",
                suggested_css="font-size: 2em; opacity: 1;",
                confidence_score=0.9,
            )
        ],
    )

    repaired_audit_result, final_result = (
        await webhook.attempt_visual_repair(
            manager,
            visual_service,
            audit_result,
            initial_result,
        )
    )

    assert manager.applied_css == [
        "font-size: 2em; opacity: 1;"
    ]

    assert len(manager.screenshots) == 1
    assert manager.screenshots[0][1] is True

    assert len(
        visual_service.prepare_inputs
    ) == 1

    assert len(
        visual_service.audit_inputs
    ) == 1

    assert (
        repaired_audit_result.screenshot_path
        == Path("artifacts/repair-job-mobile-repair-1.png")
    )

    assert final_result.defect_count == 0


@pytest.mark.asyncio
async def test_attempt_visual_repair_skips_when_no_defects() -> None:
    class FakeManager:
        def __init__(self) -> None:
            self.applied_css = False
            self.screenshot_called = False

        async def apply_css(self, css: str) -> None:
            self.applied_css = True

        async def screenshot(
            self,
            output_path: object,
            full_page: bool = True,
        ) -> object:
            self.screenshot_called = True
            return output_path

    class FakeVisualService:
        def __init__(self) -> None:
            self.audit_called = False

        def prepare_input(
            self,
            audit_result: BrowserAuditResult,
        ) -> object:
            return audit_result

        async def audit(
            self,
            audit_input: object,
        ) -> VisualAuditResponse:
            self.audit_called = True

            return VisualAuditResponse(
                job_id="clean-job",
                target_url="https://example.com",
                viewport="desktop",
                defects=[],
            )

    manager = FakeManager()
    visual_service = FakeVisualService()

    audit_result = BrowserAuditResult(
        job_id="clean-job",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path="artifacts/clean-job.png",
        dom_snapshot=(
            "<html>"
            "<body>Hello</body>"
            "</html>"
        ),
    )

    visual_result = VisualAuditResponse(
        job_id="clean-job",
        target_url="https://example.com",
        viewport="desktop",
        defects=[],
    )

    result = await webhook.attempt_visual_repair(
        manager,
        visual_service,
        audit_result,
        visual_result,
    )

    assert result == (
        audit_result,
        visual_result,
    )

    assert manager.applied_css is False
    assert manager.screenshot_called is False
    assert visual_service.audit_called is False


@pytest.mark.asyncio
async def test_attempt_visual_repair_skips_when_css_is_missing() -> None:
    class FakeManager:
        def __init__(self) -> None:
            self.applied_css = False
            self.screenshot_called = False

        async def apply_css(self, css: str) -> None:
            self.applied_css = True

        async def screenshot(
            self,
            output_path: object,
            full_page: bool = True,
        ) -> object:
            self.screenshot_called = True
            return output_path

    class FakeVisualService:
        def __init__(self) -> None:
            self.audit_called = False

        def prepare_input(
            self,
            audit_result: BrowserAuditResult,
        ) -> object:
            return audit_result

        async def audit(
            self,
            audit_input: object,
        ) -> VisualAuditResponse:
            self.audit_called = True

            return VisualAuditResponse(
                job_id="no-css-job",
                target_url="https://example.com",
                viewport="tablet",
                defects=[],
            )

    manager = FakeManager()
    visual_service = FakeVisualService()

    audit_result = BrowserAuditResult(
        job_id="no-css-job",
        target_url="https://example.com",
        viewport="tablet",
        screenshot_path="artifacts/no-css-job.png",
        dom_snapshot=(
            "<html>"
            "<body>Hello</body>"
            "</html>"
        ),
    )

    visual_result = VisualAuditResponse(
        job_id="no-css-job",
        target_url="https://example.com",
        viewport="tablet",
        defects=[
            VisualDefect(
                element_selector="div",
                defect_type="layout problem",
                description="Content is misaligned.",
                suggested_css=None,
                confidence_score=0.8,
            )
        ],
    )

    result = await webhook.attempt_visual_repair(
        manager,
        visual_service,
        audit_result,
        visual_result,
    )

    assert result == (
        audit_result,
        visual_result,
    )

    assert manager.applied_css is False
    assert manager.screenshot_called is False
    assert visual_service.audit_called is False
    

@pytest.mark.asyncio
async def test_audit_repair_loop_retries_until_success() -> None:
    class FakeManager:
        def __init__(self) -> None:
            self.applied_css: list[str] = []
            self.screenshots: list[object] = []

        async def apply_css(self, css: str) -> None:
            self.applied_css.append(css)

        async def screenshot(
            self,
            output_path: object,
            full_page: bool = True,
        ) -> object:
            self.screenshots.append(output_path)
            return output_path

        async def get_dom_snapshot(self) -> str:
            return "<html><body><h1>Example</h1></body></html>"

    class FakeVisualService:
        def __init__(self) -> None:
            self.audit_count = 0

        def prepare_input(
            self,
            audit_result: BrowserAuditResult,
        ) -> object:
            return audit_result

        async def audit(
            self,
            audit_input: object,
        ) -> VisualAuditResponse:
            self.audit_count += 1

            if self.audit_count < 3:
                return VisualAuditResponse(
                    job_id="retry-job",
                    target_url="https://example.com",
                    viewport="mobile",
                    defects=[
                        VisualDefect(
                            element_selector="h1",
                            defect_type="unreadable text",
                            description="Heading is still difficult to read.",
                            suggested_css=(
                                f"font-size: {self.audit_count + 2}em;"
                            ),
                            confidence_score=0.9,
                        )
                    ],
                )

            return VisualAuditResponse(
                job_id="retry-job",
                target_url="https://example.com",
                viewport="mobile",
                defects=[],
            )

    manager = FakeManager()
    visual_service = FakeVisualService()

    audit_result = BrowserAuditResult(
        job_id="retry-job",
        target_url="https://example.com",
        viewport="mobile",
        screenshot_path="artifacts/retry-job-mobile.png",
        dom_snapshot="<html><body><h1>Example</h1></body></html>",
    )

    initial_result = VisualAuditResponse(
        job_id="retry-job",
        target_url="https://example.com",
        viewport="mobile",
        defects=[
            VisualDefect(
                element_selector="h1",
                defect_type="unreadable text",
                description="Heading is difficult to read.",
                suggested_css="font-size: 2em;",
                confidence_score=0.9,
            )
        ],
    )

    current_audit_result = audit_result
    current_visual_result = initial_result
    max_repair_attempts = 3

    for repair_attempt in range(1, max_repair_attempts + 1):
        (
            current_audit_result,
            current_visual_result,
        ) = await webhook.attempt_visual_repair(
            manager=manager,
            visual_service=visual_service,
            audit_result=current_audit_result,
            visual_result=current_visual_result,
            repair_attempt=repair_attempt,
        )

        if current_visual_result.defect_count == 0:
            break

    assert current_visual_result.defect_count == 0
    assert visual_service.audit_count == 3

    assert manager.applied_css == [
        "font-size: 2em;",
        "font-size: 3em;",
        "font-size: 4em;",
    ]

    assert len(manager.screenshots) == 3

    assert (
        current_audit_result.screenshot_path
        == Path("artifacts/retry-job-mobile-repair-3.png")
    )

@pytest.mark.asyncio
async def test_audit_repair_loop_stops_on_duplicate_css() -> None:
    class FakeManager:
        def __init__(self) -> None:
            self.applied_css: list[str] = []

        async def apply_css(self, css: str) -> None:
            self.applied_css.append(css)

        async def screenshot(
            self,
            output_path: object,
            full_page: bool = True,
        ) -> object:
            return output_path

        async def get_dom_snapshot(self) -> str:
            return "<html><body><h1>Example</h1></body></html>"

    class FakeVisualService:
        def __init__(self) -> None:
            self.audit_count = 0

        def prepare_input(
            self,
            audit_result: BrowserAuditResult,
        ) -> object:
            return audit_result

        async def audit(
            self,
            audit_input: object,
        ) -> VisualAuditResponse:
            self.audit_count += 1

            return VisualAuditResponse(
                job_id="duplicate-job",
                target_url="https://example.com",
                viewport="mobile",
                defects=[
                    VisualDefect(
                        element_selector="h1",
                        defect_type="unreadable text",
                        description="Heading is still difficult to read.",
                        suggested_css="font-size: 2em; opacity: 1;",
                        confidence_score=0.9,
                    )
                ],
            )

    manager = FakeManager()
    visual_service = FakeVisualService()

    audit_result = BrowserAuditResult(
        job_id="duplicate-job",
        target_url="https://example.com",
        viewport="mobile",
        screenshot_path="artifacts/duplicate-job-mobile.png",
        dom_snapshot="<html><body><h1>Example</h1></body></html>",
    )

    visual_result = VisualAuditResponse(
        job_id="duplicate-job",
        target_url="https://example.com",
        viewport="mobile",
        defects=[
            VisualDefect(
                element_selector="h1",
                defect_type="unreadable text",
                description="Heading is difficult to read.",
                suggested_css="font-size: 2em; opacity: 1;",
                confidence_score=0.9,
            )
        ],
    )

    attempted_repairs: set[str] = set()
    max_repair_attempts = 3

    for repair_attempt in range(
        1,
        max_repair_attempts + 1,
    ):
        defect = visual_result.defects[0]

        if not defect.suggested_css:
            break

        if webhook._repair_was_already_attempted(
            defect.suggested_css,
            attempted_repairs,
        ):
            break

        attempted_repairs.add(
            defect.suggested_css.strip()
        )

        (
            audit_result,
            visual_result,
        ) = await webhook.attempt_visual_repair(
            manager=manager,
            visual_service=visual_service,
            audit_result=audit_result,
            visual_result=visual_result,
            repair_attempt=repair_attempt,
        )

    assert manager.applied_css == [
        "font-size: 2em; opacity: 1;"
    ]

    assert visual_service.audit_count == 1
    assert visual_result.defect_count == 1



