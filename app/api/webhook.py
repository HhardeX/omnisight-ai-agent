from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, status

from app.browser.navigator import BrowserManager
from app.models.audit import BrowserAuditResult
from app.models.jobs import BuildEvent


router = APIRouter(
    prefix="/api/v1",
    tags=["webhook"],
)


async def run_audit_job(job_id: str, event: BuildEvent) -> None:
    """
    Execute a browser-based OmniSight audit in the background.
    """
    print(
        f"[OmniSight] Starting audit job {job_id} "
        f"for {event.repository}@{event.commit_sha}"
    )

    manager = BrowserManager(headless=True)

    try:
        await manager.start(viewport="desktop")

        await manager.navigate(str(event.target_url))

        screenshot_path = Path("artifacts") / f"{job_id}-desktop.png"
        await manager.screenshot(
            screenshot_path,
            full_page=True,
        )

        dom_snapshot = await manager.get_dom_snapshot()

        h1_bounds = await manager.get_element_bounds("h1")

        element_bounds = {}

        if h1_bounds is not None:
            element_bounds["h1"] = h1_bounds

        audit_result = BrowserAuditResult(
            job_id=job_id,
            target_url=str(event.target_url),
            viewport="desktop",
            screenshot_path=screenshot_path,
            dom_snapshot=dom_snapshot,
            element_bounds=element_bounds,
        )

        print(
            f"[OmniSight] Audit job {audit_result.job_id} "
            f"completed browser capture. "
            f"DOM size: {audit_result.dom_size} characters"
        )
        print(
            f"[OmniSight] Screenshot saved: "
            f"{audit_result.screenshot_path}"
        )

    except Exception as exc:
        print(
            f"[OmniSight] Audit job {job_id} failed: "
            f"{type(exc).__name__}: {exc}"
        )
        
        print(
            f"[OmniSight] Captured element bounds: "
            f"{list(audit_result.element_bounds.keys())}"
)

    finally:
        await manager.stop()


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

    background_tasks.add_task(
        run_audit_job,
        job_id,
        event,
    )

    return {
        "job_id": job_id,
        "status": "accepted",
        "message": "Build event accepted and audit scheduled.",
    }