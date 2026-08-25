import pytest
from fastapi import BackgroundTasks

from app.api import webhook
from app.models.jobs import BuildEvent


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