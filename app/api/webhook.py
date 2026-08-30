from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, status

from app.browser.navigator import BrowserManager
from app.core.config import get_settings
from app.models.audit import BrowserAuditResult
from app.models.jobs import BuildEvent
from app.services.providers.rule_based_vlm import RuleBasedVLMProvider
from app.services.result_store import result_store
from app.services.visual_audit import VisualAuditService


router = APIRouter(
    prefix="/api/v1",
    tags=["webhook"],
)

async def attempt_visual_repair(
    manager: BrowserManager,
    visual_service: VisualAuditService,
    audit_result: BrowserAuditResult,
    visual_result,
    repair_attempt: int = 1,
) -> tuple[BrowserAuditResult, object]:
    """
    Apply the first VLM-generated CSS fix and re-run the visual audit.
    """

    if visual_result.defect_count == 0:
        return audit_result, visual_result

    defect = visual_result.defects[0]

    if not defect.suggested_css:
        print(
            f"[OmniSight] No CSS repair available for "
            f"{defect.element_selector}"
        )
        return audit_result, visual_result

    print(
        f"[OmniSight] Applying repair attempt {repair_attempt} "
        f"for {defect.element_selector}: "
        f"{defect.suggested_css}"
    )

    await manager.apply_css(
        defect.suggested_css
    )

    repaired_screenshot_path = (
        Path("artifacts")
        / (
            f"{audit_result.job_id}-"
            f"{audit_result.viewport}-"
            f"repair-{repair_attempt}.png"
        )
    )

    await manager.screenshot(
        repaired_screenshot_path,
        full_page=True,
    )

    repaired_dom_snapshot = (
        await manager.get_dom_snapshot()
    )

    repaired_audit_result = BrowserAuditResult(
        job_id=audit_result.job_id,
        target_url=audit_result.target_url,
        viewport=audit_result.viewport,
        screenshot_path=repaired_screenshot_path,
        dom_snapshot=repaired_dom_snapshot,
        element_bounds=audit_result.element_bounds,
    )

    repaired_visual_input = (
        visual_service.prepare_input(
            repaired_audit_result
        )
    )

    repaired_visual_result = (
        await visual_service.audit(
            repaired_visual_input
        )
    )

    return (
        repaired_audit_result,
        repaired_visual_result,
    )


async def run_audit_job(job_id: str, event: BuildEvent) -> None:
    """
    Execute responsive browser-based OmniSight audits.
    """

    print(
        f"[OmniSight] Starting audit job {job_id} "
        f"for {event.repository}@{event.commit_sha}"
    )

    settings = get_settings()

    if settings.vlm_provider == "ollama":
        from app.services.providers.ollama_vlm import OllamaVLMProvider

        provider = OllamaVLMProvider(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
        )
    else:
        provider = RuleBasedVLMProvider()

    visual_service = VisualAuditService(provider)

    for viewport_name in BrowserManager.VIEWPORTS:
        manager = BrowserManager(headless=True)

        try:
            print(
                f"[OmniSight] Starting {viewport_name} audit "
                f"for job {job_id}"
            )

            await manager.start(
                viewport=viewport_name
            )

            await manager.navigate(
                str(event.target_url)
            )

            screenshot_path = (
                Path("artifacts")
                / f"{job_id}-{viewport_name}.png"
            )

            await manager.screenshot(
                screenshot_path,
                full_page=True,
            )

            dom_snapshot = (
                await manager.get_dom_snapshot()
            )

            h1_bounds = (
                await manager.get_element_bounds("h1")
            )

            element_bounds = {}

            if h1_bounds is not None:
                element_bounds["h1"] = h1_bounds

            audit_result = BrowserAuditResult(
                job_id=job_id,
                target_url=str(event.target_url),
                viewport=viewport_name,
                screenshot_path=screenshot_path,
                dom_snapshot=dom_snapshot,
                element_bounds=element_bounds,
            )

            print(
                f"[OmniSight] {viewport_name} browser capture "
                f"completed. "
                f"DOM size: {audit_result.dom_size} characters"
            )

            print(
                f"[OmniSight] Screenshot saved: "
                f"{audit_result.screenshot_path}"
            )

            visual_input = (
                visual_service.prepare_input(
                    audit_result
                )
            )

            visual_result = await visual_service.audit(
                visual_input
            )

            result_store.save(
                audit_result,
                visual_result,
            )

            print(
                f"[OmniSight] {viewport_name} visual audit "
                f"completed. "
                f"Defects detected: "
                f"{visual_result.defect_count}"
            )

            for defect in visual_result.defects:
                print(
                    f"[OmniSight] Defect: "
                    f"{defect.defect_type} | "
                    f"{defect.element_selector} | "
                    f"{defect.description}"
                )

        except Exception as exc:
            print(
                f"[OmniSight] {viewport_name} audit failed "
                f"for job {job_id}: "
                f"{type(exc).__name__}: {exc}"
            )

        finally:
            await manager.stop()

    print(
        f"[OmniSight] Responsive audit job "
        f"{job_id} completed."
    )


@router.post(
    "/build-event",
    status_code=status.HTTP_202_ACCEPTED,
)
async def receive_build_event(
    event: BuildEvent,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    """
    Receive a CI/CD build event and schedule an asynchronous audit.
    """

    job_id = str(uuid4())

    print(
        f"[OmniSight] Scheduling audit job {job_id}"
    )

    background_tasks.add_task(
        run_audit_job,
        job_id,
        event,
    )

    return {
        "job_id": job_id,
        "status": "accepted",
        "message": (
            "Build event accepted and responsive "
            "audit scheduled."
        ),
    }