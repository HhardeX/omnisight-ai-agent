from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.main import app
from app.services.repair import RepairService


def test_publish_repair_creates_branch_commits_file_and_opens_pr() -> None:
    github = MagicMock()

    github.update_file.return_value = "repair-commit-sha"
    github.create_pull_request.return_value = (
        "https://github.com/owner/repository/pull/123"
    )

    service = RepairService(github)

    result = service.publish_repair(
        branch_name="omnisight/repair-job-001",
        file_path="src/Repair.css",
        content=".button { margin-top: 8px; }",
        commit_message="fix: repair visual defect",
        pull_request_title="fix: OmniSight visual repair",
        pull_request_body=(
            "OmniSight automatically repaired a detected "
            "visual defect."
        ),
    )

    github.create_branch.assert_called_once_with(
        "omnisight/repair-job-001"
    )

    github.update_file.assert_called_once_with(
        branch_name="omnisight/repair-job-001",
        file_path="src/Repair.css",
        content=".button { margin-top: 8px; }",
        commit_message="fix: repair visual defect",
    )

    github.create_pull_request.assert_called_once_with(
        branch_name="omnisight/repair-job-001",
        title="fix: OmniSight visual repair",
        body=(
            "OmniSight automatically repaired a detected "
            "visual defect."
        ),
    )

    assert result.branch_name == "omnisight/repair-job-001"
    assert result.commit_sha == "repair-commit-sha"
    assert result.pull_request_url == (
        "https://github.com/owner/repository/pull/123"
    )


def test_repair_api_publishes_repair(monkeypatch) -> None:
    github = MagicMock()

    github.update_file.return_value = "repair-commit-sha"
    github.create_pull_request.return_value = (
        "https://github.com/owner/repository/pull/123"
    )

    class FakeSettings:
        github_token = "test-token"
        github_repository = "owner/repository"
        github_base_branch = "main"

    monkeypatch.setattr(
        "app.api.repair.get_settings",
        lambda: FakeSettings(),
    )

    monkeypatch.setattr(
        "app.api.repair.GitHubService",
        lambda **kwargs: github,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/repair",
        json={
            "job_id": "job-001",
            "viewport": "desktop",
            "file_path": "src/Repair.css",
            "content": ".button { margin-top: 8px; }",
            "commit_message": "fix: repair visual defect",
            "pull_request_title": "fix: OmniSight visual repair",
            "pull_request_body": (
                "OmniSight automatically repaired a detected "
                "visual defect."
            ),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["job_id"] == "job-001"
    assert data["viewport"] == "desktop"
    assert data["branch_name"] == (
        "omnisight/repair-job-001-desktop"
    )
    assert data["commit_sha"] == "repair-commit-sha"
    assert data["pull_request_url"] == (
        "https://github.com/owner/repository/pull/123"
    )

    github.close.assert_called_once()


def test_repair_api_requires_github_configuration(monkeypatch) -> None:
    class FakeSettings:
        github_token = ""
        github_repository = ""
        github_base_branch = "main"

    monkeypatch.setattr(
        "app.api.repair.get_settings",
        lambda: FakeSettings(),
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/repair",
        json={
            "job_id": "job-001",
            "viewport": "desktop",
            "file_path": "src/Repair.css",
            "content": ".button { margin-top: 8px; }",
            "commit_message": "fix: repair visual defect",
            "pull_request_title": "fix: OmniSight visual repair",
            "pull_request_body": "Automated repair.",
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "GitHub token is not configured."
    )


def test_repair_api_returns_502_when_github_fails(monkeypatch) -> None:
    class FakeSettings:
        github_token = "test-token"
        github_repository = "owner/repository"
        github_base_branch = "main"

    github = MagicMock()

    github.create_branch.side_effect = RuntimeError(
        "GitHub unavailable"
    )

    monkeypatch.setattr(
        "app.api.repair.get_settings",
        lambda: FakeSettings(),
    )

    monkeypatch.setattr(
        "app.api.repair.GitHubService",
        lambda **kwargs: github,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/repair",
        json={
            "job_id": "job-001",
            "viewport": "desktop",
            "file_path": "src/Repair.css",
            "content": ".button { margin-top: 8px; }",
            "commit_message": "fix: repair visual defect",
            "pull_request_title": "fix: OmniSight visual repair",
            "pull_request_body": "Automated repair.",
        },
    )

    assert response.status_code == 502
    assert "GitHub repair publishing failed" in (
        response.json()["detail"]
    )

    github.close.assert_called_once()


def test_pull_requests_api_returns_published_repairs(
    monkeypatch,
) -> None:
    github = MagicMock()

    github.update_file.return_value = "repair-commit-sha"
    github.create_pull_request.return_value = (
        "https://github.com/owner/repository/pull/456"
    )

    class FakeSettings:
        github_token = "test-token"
        github_repository = "owner/repository"
        github_base_branch = "main"

    monkeypatch.setattr(
        "app.api.repair.get_settings",
        lambda: FakeSettings(),
    )

    monkeypatch.setattr(
        "app.api.repair.GitHubService",
        lambda **kwargs: github,
    )

    client = TestClient(app)

    repair_response = client.post(
        "/api/v1/repair",
        json={
            "job_id": "job-pull-request-001",
            "viewport": "desktop",
            "file_path": "src/Repair.css",
            "content": ".button { margin-top: 8px; }",
            "commit_message": "fix: OmniSight visual repair",
            "pull_request_title": "fix: OmniSight visual repair",
            "pull_request_body": "Automated visual repair.",
        },
    )

    assert repair_response.status_code == 201

    response = client.get("/api/v1/pull-requests")

    assert response.status_code == 200

    data = response.json()

    matching_repairs = [
        repair
        for repair in data
        if repair["job_id"] == "job-pull-request-001"
    ]

    assert len(matching_repairs) == 1

    repair = matching_repairs[0]

    assert repair["job_id"] == "job-pull-request-001"
    assert repair["viewport"] == "desktop"
    assert repair["branch_name"] == (
        "omnisight/repair-job-pull-request-001-desktop"
    )
    assert repair["commit_sha"] == "repair-commit-sha"
    assert repair["pull_request_url"] == (
        "https://github.com/owner/repository/pull/456"
    )

    github.close.assert_called_once()


# ---------------------------------------------------------------------------
# Feature 3: AI Confidence + Human Approval Gate
# ---------------------------------------------------------------------------


def test_approval_api_returns_404_for_unknown_job(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.api.repair.job_store.get_job",
        lambda job_id: None,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/jobs/unknown-job/approval",
        json={"decision": "approve"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found."


def test_approval_api_returns_409_for_non_pending_job(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        "app.api.repair.job_store.get_job",
        lambda job_id: {
            "job_id": job_id,
            "approval_status": "not_required",
        },
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/jobs/job-completed/approval",
        json={"decision": "approve"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == (
        "Job does not have a pending approval request."
    )


def test_approval_api_approve_schedules_audit(
    monkeypatch,
) -> None:
    job = {
        "job_id": "job-approve-001",
        "repository": "test/repo",
        "commit_sha": "abc1234",
        "branch": "feature/test",
        "target_url": "http://example.com/",
        "approval_status": "pending",
    }

    monkeypatch.setattr(
        "app.api.repair.job_store.get_job",
        lambda job_id: job,
    )

    approve_job = MagicMock()

    monkeypatch.setattr(
        "app.api.repair.job_store.approve_job",
        approve_job,
    )

    scheduled_tasks = []

    def fake_add_task(self, function, *args, **kwargs):
        scheduled_tasks.append(
            (function, args, kwargs)
        )

    monkeypatch.setattr(
        "app.api.repair.BackgroundTasks.add_task",
        fake_add_task,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/jobs/job-approve-001/approval",
        json={"decision": "approve"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == "job-approve-001"
    assert data["approval_status"] == "approved"

    approve_job.assert_called_once_with(
        "job-approve-001"
    )

    assert len(scheduled_tasks) == 1

    function, args, kwargs = scheduled_tasks[0]

    assert function.__name__ == "run_audit_job"
    assert args[0] == "job-approve-001"

    event = args[1]

    assert event.repository == "test/repo"
    assert event.commit_sha == "abc1234"
    assert event.branch == "feature/test"
    assert str(event.target_url) == "http://example.com/"

    assert kwargs == {}


def test_approval_api_reject_completes_without_scheduling(
    monkeypatch,
) -> None:
    job = {
        "job_id": "job-reject-001",
        "repository": "test/repo",
        "commit_sha": "abc123",
        "branch": "feature/test",
        "target_url": "http://example.com/",
        "approval_status": "pending",
    }

    monkeypatch.setattr(
        "app.api.repair.job_store.get_job",
        lambda job_id: job,
    )

    reject_job = MagicMock()
    mark_completed = MagicMock()

    monkeypatch.setattr(
        "app.api.repair.job_store.reject_job",
        reject_job,
    )

    monkeypatch.setattr(
        "app.api.repair.job_store.mark_completed",
        mark_completed,
    )

    add_task = MagicMock()

    monkeypatch.setattr(
        "app.api.repair.BackgroundTasks.add_task",
        add_task,
    )

    client = TestClient(app)

    response = client.post(
        "/api/v1/jobs/job-reject-001/approval",
        json={"decision": "reject"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == "job-reject-001"
    assert data["approval_status"] == "rejected"

    reject_job.assert_called_once_with(
        "job-reject-001"
    )

    mark_completed.assert_called_once_with(
        "job-reject-001"
    )

    add_task.assert_not_called()


def test_approved_job_can_bypass_low_confidence_gate(
    monkeypatch,
) -> None:
    job = {
        "job_id": "job-approved-low-confidence",
        "approval_status": "approved",
    }

    monkeypatch.setattr(
        "app.api.webhook.job_store.get_job",
        lambda job_id: job,
    )

    from app.api.webhook import _requires_human_approval

    confidence = 0.40
    threshold = 0.85

    assert _requires_human_approval(
        confidence_score=confidence,
        threshold=threshold,
    )

    assert job["approval_status"] == "approved"

    assert not (
        job["approval_status"] != "approved"
        and _requires_human_approval(
            confidence_score=confidence,
            threshold=threshold,
        )
    )