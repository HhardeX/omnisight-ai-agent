from unittest.mock import MagicMock

from app.services.repair import RepairService
from fastapi.testclient import TestClient

from app.main import app



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