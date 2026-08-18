from fastapi import APIRouter

from app.services.result_store import result_store


router = APIRouter(
    prefix="/api/v1",
    tags=["results"],
)


@router.get("/builds")
async def get_builds() -> list[dict]:
    results = result_store.get_all_browser_results()

    return [
        {
            "job_id": result.job_id,
            "target_url": result.target_url,
            "viewport": result.viewport,
            "dom_size": result.dom_size,
        }
        for result in results
    ]


@router.get("/issues")
async def get_issues() -> list[dict]:
    results = result_store.get_all_visual_results()

    issues = []

    for result in results:
        for defect in result.defects:
            issues.append(
                {
                    "job_id": result.job_id,
                    "target_url": result.target_url,
                    "viewport": result.viewport,
                    "element_selector": defect.element_selector,
                    "defect_type": defect.defect_type,
                    "description": defect.description,
                    "suggested_css": defect.suggested_css,
                    "confidence_score": defect.confidence_score,
                    "bounding_box": (
                        defect.bounding_box.model_dump()
                        if defect.bounding_box
                        else None
                    ),
                }
            )

    return issues


@router.get("/screenshots")
async def get_screenshots() -> list[dict]:
    results = result_store.get_all_browser_results()

    return [
        {
            "job_id": result.job_id,
            "target_url": result.target_url,
            "viewport": result.viewport,
            "screenshot_path": str(result.screenshot_path),
        }
        for result in results
    ]


@router.get("/dashboard")
async def get_dashboard() -> dict:
    browser_results = result_store.get_all_browser_results()
    visual_results = result_store.get_all_visual_results()

    total_issues = sum(
        result.defect_count
        for result in visual_results
    )

    latest_build = None

    if browser_results:
        latest = browser_results[-1]

        latest_build = {
            "job_id": latest.job_id,
            "target_url": latest.target_url,
            "viewport": latest.viewport,
            "dom_size": latest.dom_size,
        }

    return {
        "total_builds": len(browser_results),
        "total_issues": total_issues,
        "total_screenshots": len(browser_results),
        "latest_build": latest_build,
    }