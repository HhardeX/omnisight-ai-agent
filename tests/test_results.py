from pathlib import Path

import pytest

from app.api import results
from app.models.audit import BrowserAuditResult, ElementBounds
from app.models.visual import VisualAuditResponse, VisualDefect
from app.services.result_store import AuditResultStore
from app.models.jobs import BuildEvent
from app.services.job_store import JobStore


def make_browser_result(
    job_id: str,
    target_url: str = "https://example.com",
) -> BrowserAuditResult:
    return BrowserAuditResult(
        job_id=job_id,
        target_url=target_url,
        viewport="desktop",
        screenshot_path=Path(f"artifacts/{job_id}.png"),
        dom_snapshot="<html><body>Hello</body></html>",
    )


def make_visual_result(
    job_id: str,
    target_url: str = "https://example.com",
    defects: list[VisualDefect] | None = None,
) -> VisualAuditResponse:
    return VisualAuditResponse(
        job_id=job_id,
        target_url=target_url,
        viewport="desktop",
        defects=defects or [],
    )


@pytest.mark.asyncio
async def test_get_builds_returns_browser_results() -> None:
    store = AuditResultStore()
    store.save(
        make_browser_result("job-1"),
        make_visual_result("job-1"),
    )

    original_store = results.result_store
    results.result_store = store

    try:
        response = await results.get_builds()
    finally:
        results.result_store = original_store

    assert response == [
        {
            "job_id": "job-1",
            "target_url": "https://example.com",
            "viewport": "desktop",
            "dom_size": len("<html><body>Hello</body></html>"),
        }
    ]


@pytest.mark.asyncio
async def test_get_issues_flattens_visual_defects() -> None:
    store = AuditResultStore()

    defect = VisualDefect(
        element_selector="#login",
        defect_type="overlap",
        description="Login button overlaps the form.",
        suggested_css="margin-top: 8px;",
        confidence_score=0.95,
        bounding_box=ElementBounds(
            x=10,
            y=20,
            width=100,
            height=40,
        ),
    )

    store.save(
        make_browser_result("job-1"),
        make_visual_result(
            "job-1",
            defects=[defect],
        ),
    )

    original_store = results.result_store
    results.result_store = store

    try:
        response = await results.get_issues()
    finally:
        results.result_store = original_store

    assert response == [
        {
            "job_id": "job-1",
            "target_url": "https://example.com",
            "viewport": "desktop",
            "element_selector": "#login",
            "defect_type": "overlap",
            "description": "Login button overlaps the form.",
            "suggested_css": "margin-top: 8px;",
            "confidence_score": 0.95,
            "bounding_box": {
                "x": 10.0,
                "y": 20.0,
                "width": 100.0,
                "height": 40.0,
            },
        }
    ]


@pytest.mark.asyncio
async def test_get_screenshots_returns_screenshot_paths() -> None:
    store = AuditResultStore()
    store.save(
        make_browser_result("job-1"),
        make_visual_result("job-1"),
    )

    original_store = results.result_store
    results.result_store = store

    try:
        response = await results.get_screenshots()
    finally:
        results.result_store = original_store

    assert response == [
        {
            "job_id": "job-1",
            "target_url": "https://example.com",
            "viewport": "desktop",
            "screenshot_path": str(Path("artifacts/job-1.png")),
        }
    ]


@pytest.mark.asyncio
async def test_get_dashboard_returns_summary_and_latest_build() -> None:
    store = AuditResultStore()

    store.save(
        make_browser_result("job-1"),
        make_visual_result("job-1"),
    )

    defect = VisualDefect(
        element_selector="#submit",
        defect_type="misalignment",
        description="Submit button is misaligned.",
        confidence_score=0.9,
    )

    store.save(
        make_browser_result(
            "job-2",
            "https://example.org",
        ),
        make_visual_result(
            "job-2",
            "https://example.org",
            defects=[defect],
        ),
    )

    original_store = results.result_store
    results.result_store = store

    try:
        response = await results.get_dashboard()
    finally:
        results.result_store = original_store

    assert response == {
        "total_builds": 2,
        "total_issues": 1,
        "total_screenshots": 2,
        "latest_build": {
            "job_id": "job-2",
            "target_url": "https://example.org",
            "viewport": "desktop",
            "dom_size": len("<html><body>Hello</body></html>"),
        },
    }


@pytest.mark.asyncio
async def test_get_dashboard_returns_empty_summary_when_store_is_empty() -> None:
    store = AuditResultStore()

    original_store = results.result_store
    results.result_store = store

    try:
        response = await results.get_dashboard()
    finally:
        results.result_store = original_store

    assert response == {
        "total_builds": 0,
        "total_issues": 0,
        "total_screenshots": 0,
        "latest_build": None,
    }
    
@pytest.mark.asyncio
async def test_get_jobs_returns_persisted_job_history(
    tmp_path,
    monkeypatch,
) -> None:
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.db.database.DATABASE_PATH",
        database_path,
    )

    from app.db.database import initialize_database

    initialize_database()

    store = JobStore()

    event = BuildEvent(
        repository="test/repo",
        commit_sha="abc1234",
        branch="feature/test",
        target_url="https://example.com",
    )

    store.create_job("job-1", event)
    store.mark_running("job-1")
    store.mark_completed("job-1")

    original_store = results.job_store
    results.job_store = store

    try:
        response = await results.get_jobs()
    finally:
        results.job_store = original_store

    assert len(response) == 1
    assert response[0]["job_id"] == "job-1"
    assert response[0]["repository"] == "test/repo"
    assert response[0]["commit_sha"] == "abc1234"
    assert response[0]["branch"] == "feature/test"
    assert response[0]["status"] == "completed"
    assert response[0]["error_message"] is None
    assert response[0]["started_at"] is not None
    assert response[0]["completed_at"] is not None


@pytest.mark.asyncio
async def test_get_job_returns_specific_job(
    tmp_path,
    monkeypatch,
) -> None:
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        "app.db.database.DATABASE_PATH",
        database_path,
    )

    from app.db.database import initialize_database

    initialize_database()

    store = JobStore()

    event = BuildEvent(
        repository="test/repo",
        commit_sha="abc1234",
        branch="feature/test",
        target_url="https://example.com",
    )

    store.create_job("job-1", event)

    original_store = results.job_store
    results.job_store = store

    try:
        response = await results.get_job("job-1")
    finally:
        results.job_store = original_store

    assert response is not None
    assert response["job_id"] == "job-1"
    assert response["status"] == "queued"
    assert response["repository"] == "test/repo"
    