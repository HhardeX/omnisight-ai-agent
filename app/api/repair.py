from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.api.webhook import run_audit_job
from app.core.config import get_settings
from app.models.jobs import BuildEvent
from app.models.repair import (
    ApprovalRequest,
    ApprovalResponse,
    RepairRequest,
    RepairResponse,
)
from app.services.github import GitHubService
from app.services.repair import RepairService
from app.services.result_store import PublishedRepair, result_store
from app.services.job_store import job_store


router = APIRouter(
    prefix="/api/v1",
    tags=["repair"],
)


@router.post(
    "/repair",
    response_model=RepairResponse,
    status_code=status.HTTP_201_CREATED,
)
async def publish_repair(
    request: RepairRequest,
) -> RepairResponse:
    """Publish a validated visual repair to GitHub."""

    settings = get_settings()

    if not settings.github_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitHub token is not configured.",
        )

    if not settings.github_repository:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GitHub repository is not configured.",
        )

    github_service = GitHubService(
        token=settings.github_token,
        repository=settings.github_repository,
        base_branch=settings.github_base_branch,
    )

    repair_service = RepairService(github_service)

    branch_name = (
        f"omnisight/repair-"
        f"{request.job_id}-"
        f"{request.viewport}"
    )

    try:
        result = repair_service.publish_repair(
            branch_name=branch_name,
            file_path=request.file_path,
            content=request.content,
            commit_message=request.commit_message,
            pull_request_title=request.pull_request_title,
            pull_request_body=request.pull_request_body,
        )

        published_repair = PublishedRepair(
            job_id=request.job_id,
            viewport=request.viewport,
            branch_name=result.branch_name,
            commit_sha=result.commit_sha,
            pull_request_url=result.pull_request_url,
        )

        result_store.save_published_repair(
            published_repair
        )

        return RepairResponse(
            job_id=request.job_id,
            viewport=request.viewport,
            branch_name=result.branch_name,
            commit_sha=result.commit_sha,
            pull_request_url=result.pull_request_url,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub repair publishing failed: {exc}",
        ) from exc

    finally:
        github_service.close()


@router.post(
    "/jobs/{job_id}/approval",
    response_model=ApprovalResponse,
)
async def update_job_approval(
    job_id: str,
    request: ApprovalRequest,
    background_tasks: BackgroundTasks,
) -> ApprovalResponse:
    """Approve or reject a pending repair."""

    job = job_store.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found.",
        )

    if job["approval_status"] != "pending":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                "Job does not have a pending "
                "approval request."
            ),
        )

    if request.decision == "reject":
        job_store.reject_job(job_id)
        job_store.mark_completed(job_id)

        return ApprovalResponse(
            job_id=job_id,
            approval_status="rejected",
        )

    job_store.approve_job(job_id)

    event = BuildEvent(
        repository=job["repository"],
        commit_sha=job["commit_sha"],
        branch=job["branch"],
        target_url=job["target_url"],
    )

    background_tasks.add_task(
        run_audit_job,
        job_id,
        event,
    )

    return ApprovalResponse(
        job_id=job_id,
        approval_status="approved",
    )


@router.get("/pull-requests")
async def get_pull_requests() -> list[dict]:
    """Return successfully published repair pull requests."""

    return [
        {
            "job_id": repair.job_id,
            "viewport": repair.viewport,
            "branch_name": repair.branch_name,
            "commit_sha": repair.commit_sha,
            "pull_request_url": repair.pull_request_url,
        }
        for repair in result_store.get_all_published_repairs()
    ]