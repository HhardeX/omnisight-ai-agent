from unittest.mock import MagicMock, patch

import pytest
from github.GithubException import GithubException

from app.services.github import GitHubService


def make_service() -> GitHubService:
    """Create a GitHub service with a mocked client."""

    with patch(
        "app.services.github.Github"
    ) as github_class:
        github_client = github_class.return_value
        repository = MagicMock()

        github_client.get_repo.return_value = repository

        service = GitHubService(
            token="test-token",
            repository="owner/repository",
            base_branch="main",
        )

        service.github = github_client
        service.repository = repository

        return service


def test_github_service_rejects_empty_token() -> None:
    with pytest.raises(
        ValueError,
        match="GitHub token cannot be empty",
    ):
        GitHubService(
            token="",
            repository="owner/repository",
        )


def test_github_service_rejects_empty_repository() -> None:
    with pytest.raises(
        ValueError,
        match="GitHub repository cannot be empty",
    ):
        GitHubService(
            token="test-token",
            repository="",
        )


def test_github_service_rejects_empty_base_branch() -> None:
    with pytest.raises(
        ValueError,
        match="GitHub base branch cannot be empty",
    ):
        GitHubService(
            token="test-token",
            repository="owner/repository",
            base_branch="",
        )


def test_create_branch() -> None:
    service = make_service()

    base_ref = MagicMock()
    base_ref.object.sha = "base-sha"

    service.repository.get_git_ref.return_value = base_ref

    service.create_branch("omnisight/repair-job-001")

    service.repository.get_git_ref.assert_called_once_with(
        "heads/main"
    )

    service.repository.create_git_ref.assert_called_once_with(
        ref="refs/heads/omnisight/repair-job-001",
        sha="base-sha",
    )


def test_create_branch_rejects_empty_branch() -> None:
    service = make_service()

    with pytest.raises(
        ValueError,
        match="GitHub branch name cannot be empty",
    ):
        service.create_branch("")


def test_update_existing_file() -> None:
    service = make_service()

    existing_file = MagicMock()
    existing_file.sha = "old-file-sha"

    service.repository.get_contents.return_value = (
        existing_file
    )

    commit = MagicMock()
    commit.sha = "new-commit-sha"

    service.repository.update_file.return_value = {
        "commit": commit
    }

    result = service.update_file(
        branch_name="omnisight/repair-job-001",
        file_path="src/App.jsx",
        content="<button>Fixed</button>",
        commit_message="fix: repair visual defect",
    )

    assert result == "new-commit-sha"

    service.repository.get_contents.assert_called_once_with(
        "src/App.jsx",
        ref="omnisight/repair-job-001",
    )

    service.repository.update_file.assert_called_once_with(
        path="src/App.jsx",
        message="fix: repair visual defect",
        content="<button>Fixed</button>",
        sha="old-file-sha",
        branch="omnisight/repair-job-001",
    )


def test_update_missing_file_creates_file() -> None:
    service = make_service()

    service.repository.get_contents.side_effect = (
        GithubException(
            status=404,
            data={},
        )
    )

    commit = MagicMock()
    commit.sha = "created-file-commit-sha"

    service.repository.create_file.return_value = {
        "commit": commit
    }

    result = service.update_file(
        branch_name="omnisight/repair-job-001",
        file_path="src/Repair.css",
        content=".button { margin-top: 8px; }",
        commit_message="fix: add visual repair",
    )

    assert result == "created-file-commit-sha"

    service.repository.create_file.assert_called_once_with(
        path="src/Repair.css",
        message="fix: add visual repair",
        content=".button { margin-top: 8px; }",
        branch="omnisight/repair-job-001",
    )


def test_create_pull_request() -> None:
    service = make_service()

    pull_request = MagicMock()
    pull_request.html_url = (
        "https://github.com/owner/repository/pull/123"
    )

    service.repository.create_pull.return_value = (
        pull_request
    )

    result = service.create_pull_request(
        branch_name="omnisight/repair-job-001",
        title="fix: repair visual defect",
        body="OmniSight automatically repaired a visual defect.",
    )

    assert result == (
        "https://github.com/owner/repository/pull/123"
    )

    service.repository.create_pull.assert_called_once_with(
        title="fix: repair visual defect",
        body="OmniSight automatically repaired a visual defect.",
        head="omnisight/repair-job-001",
        base="main",
    )


def test_create_pull_request_rejects_empty_branch() -> None:
    service = make_service()

    with pytest.raises(
        ValueError,
        match="GitHub branch name cannot be empty",
    ):
        service.create_pull_request(
            branch_name="",
            title="test",
            body="test",
        )


def test_create_pull_request_rejects_empty_title() -> None:
    service = make_service()

    with pytest.raises(
        ValueError,
        match="Pull request title cannot be empty",
    ):
        service.create_pull_request(
            branch_name="repair",
            title="",
            body="test",
        )