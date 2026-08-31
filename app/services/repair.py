from __future__ import annotations

from dataclasses import dataclass

from app.services.github import GitHubService


@dataclass(frozen=True, slots=True)
class RepairResult:
    """Result produced after publishing a visual repair to GitHub."""

    branch_name: str
    commit_sha: str
    pull_request_url: str


class RepairService:
    """Coordinates GitHub publishing for validated visual repairs."""

    def __init__(self, github_service: GitHubService) -> None:
        self._github = github_service

    def publish_repair(
        self,
        branch_name: str,
        file_path: str,
        content: str,
        commit_message: str,
        pull_request_title: str,
        pull_request_body: str,
    ) -> RepairResult:
        """Create a repair branch, commit the repaired file, and open a PR."""

        self._github.create_branch(branch_name)

        commit_sha = self._github.update_file(
            branch_name=branch_name,
            file_path=file_path,
            content=content,
            commit_message=commit_message,
        )

        pull_request_url = self._github.create_pull_request(
            branch_name=branch_name,
            title=pull_request_title,
            body=pull_request_body,
        )

        return RepairResult(
            branch_name=branch_name,
            commit_sha=commit_sha,
            pull_request_url=pull_request_url,
        )