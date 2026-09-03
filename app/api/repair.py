from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.models.repair import RepairRequest, RepairResponse
from app.services.github import GitHubService
from app.services.repair import RepairService
from app.services.result_store import PublishedRepair, result_store


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

        result_store.save_published_repair(published_repair)

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