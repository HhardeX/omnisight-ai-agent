from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, status

from app.browser.navigator import BrowserManager
from app.models.audit import BrowserAuditResult
from app.models.jobs import BuildEvent
from app.services.providers.factory import create_vlm_provider
from app.services.result_store import result_store
from app.services.visual_audit import VisualAuditService


router = APIRouter(
    prefix="/api/v1",
    tags=["webhook"],
)


async def run_audit_job(job_id: str, event: BuildEvent) -> None:
    """
    Execute responsive browser-based OmniSight audits.
    """

    print(
        f"[OmniSight] Starting audit job {job_id} "
        f"for {event.repository}@{event.commit_sha}"
    )

    visual_service = VisualAuditService(
        create_vlm_provider()
    )

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
