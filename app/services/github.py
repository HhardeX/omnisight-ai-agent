from __future__ import annotations

from dataclasses import dataclass

from github import Github
from github.GithubException import GithubException


@dataclass(frozen=True, slots=True)
class PullRequestResult:
    """Result returned after creating a GitHub pull request."""

    branch_name: str
    commit_sha: str
    pull_request_url: str


class GitHubService:
    """Handles GitHub branch, commit, and pull-request operations."""

    def __init__(
        self,
        token: str,
        repository: str,
        base_branch: str = "main",
    ) -> None:
        if not token.strip():
            raise ValueError("GitHub token cannot be empty.")

        if not repository.strip():
            raise ValueError(
                "GitHub repository cannot be empty."
            )

        if not base_branch.strip():
            raise ValueError(
                "GitHub base branch cannot be empty."
            )

        self.token = token
        self.repository_name = repository
        self.base_branch = base_branch

        self.github = Github(token)
        self.repository = self.github.get_repo(
            repository
        )

    def create_branch(
        self,
        branch_name: str,
    ) -> None:
        """Create a new branch from the configured base branch."""

        if not branch_name.strip():
            raise ValueError(
                "GitHub branch name cannot be empty."
            )

        base_ref = self.repository.get_git_ref(
            f"heads/{self.base_branch}"
        )

        self.repository.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=base_ref.object.sha,
        )

    def update_file(
        self,
        branch_name: str,
        file_path: str,
        content: str,
        commit_message: str,
    ) -> str:
        """Create or update a repository file on a branch."""

        if not file_path.strip():
            raise ValueError(
                "GitHub file path cannot be empty."
            )

        if not commit_message.strip():
            raise ValueError(
                "GitHub commit message cannot be empty."
            )

        try:
            existing_file = self.repository.get_contents(
                file_path,
                ref=branch_name,
            )

            if isinstance(existing_file, list):
                raise ValueError(
                    f"GitHub path '{file_path}' is a directory."
                )

            result = self.repository.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=existing_file.sha,
                branch=branch_name,
            )

        except GithubException as exc:
            if exc.status != 404:
                raise

            result = self.repository.create_file(
                path=file_path,
                message=commit_message,
                content=content,
                branch=branch_name,
            )

        return result["commit"].sha

    def create_pull_request(
        self,
        branch_name: str,
        title: str,
        body: str,
    ) -> str:
        """Create a pull request from the repair branch."""

        if not branch_name.strip():
            raise ValueError(
                "GitHub branch name cannot be empty."
            )

        if not title.strip():
            raise ValueError(
                "Pull request title cannot be empty."
            )

        pull_request = self.repository.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base=self.base_branch,
        )

        return pull_request.html_url

    def close(self) -> None:
        """Release the GitHub client resources."""

        self.github.close()