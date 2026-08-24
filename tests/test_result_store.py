from pathlib import Path

from app.models.audit import BrowserAuditResult
from app.models.visual import VisualAuditResponse
from app.services.result_store import AuditResultStore


def make_browser_result(
    job_id: str,
    target_url: str = "https://example.com",
) -> BrowserAuditResult:
    return BrowserAuditResult(
        job_id=job_id,
        target_url=target_url,
        viewport="desktop",
        screenshot_path=Path(f"artifacts/{job_id}.png"),
        dom_snapshot="<html></html>",
    )


def make_visual_result(
    job_id: str,
    target_url: str = "https://example.com",
) -> VisualAuditResponse:
    return VisualAuditResponse(
        job_id=job_id,
        target_url=target_url,
        viewport="desktop",
    )


def test_save_and_get_browser_result() -> None:
    store = AuditResultStore()
    browser_result = make_browser_result("job-1")

    store.save(
        browser_result,
        make_visual_result("job-1"),
    )

    assert store.get_browser_result("job-1") == browser_result


def test_save_and_get_visual_result() -> None:
    store = AuditResultStore()
    visual_result = make_visual_result("job-1")

    store.save(
        make_browser_result("job-1"),
        visual_result,
    )

    assert store.get_visual_result("job-1") == visual_result


def test_get_unknown_job_returns_none() -> None:
    store = AuditResultStore()

    assert store.get_browser_result("missing-job") is None
    assert store.get_visual_result("missing-job") is None


def test_get_all_results_returns_saved_results() -> None:
    store = AuditResultStore()

    browser_result_1 = make_browser_result("job-1")
    browser_result_2 = make_browser_result("job-2")
    visual_result_1 = make_visual_result("job-1")
    visual_result_2 = make_visual_result("job-2")

    store.save(browser_result_1, visual_result_1)
    store.save(browser_result_2, visual_result_2)

    assert store.get_all_browser_results() == [
        browser_result_1,
        browser_result_2,
    ]
    assert store.get_all_visual_results() == [
        visual_result_1,
        visual_result_2,
    ]


def test_save_replaces_results_with_same_job_id() -> None:
    store = AuditResultStore()

    first_browser_result = make_browser_result(
        "job-1",
        "https://first.example.com",
    )
    second_browser_result = make_browser_result(
        "job-1",
        "https://second.example.com",
    )

    first_visual_result = make_visual_result(
        "job-1",
        "https://first.example.com",
    )
    second_visual_result = make_visual_result(
        "job-1",
        "https://second.example.com",
    )

    store.save(first_browser_result, first_visual_result)
    store.save(second_browser_result, second_visual_result)

    assert store.get_browser_result("job-1") == second_browser_result
    assert store.get_visual_result("job-1") == second_visual_result
    assert store.get_all_browser_results() == [second_browser_result]
    assert store.get_all_visual_results() == [second_visual_result]