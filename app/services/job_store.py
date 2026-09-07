from datetime import datetime, timezone

from app.db.database import get_connection
from app.models.jobs import BuildEvent


class JobStore:
    """Persists OmniSight job lifecycle and status information."""

    def create_job(
        self,
        job_id: str,
        event: BuildEvent,
    ) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                INSERT INTO jobs (
                    job_id,
                    repository,
                    commit_sha,
                    branch,
                    target_url,
                    status,
                    error_message,
                    created_at,
                    started_at,
                    completed_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    event.repository,
                    event.commit_sha,
                    event.branch,
                    str(event.target_url),
                    "queued",
                    None,
                    self._now(),
                    None,
                    None,
                ),
            )

            connection.commit()
        finally:
            connection.close()

    def mark_running(self, job_id: str) -> None:
        self._update_status(
            job_id=job_id,
            status="running",
            started_at=self._now(),
        )

    def mark_completed(self, job_id: str) -> None:
        self._update_status(
            job_id=job_id,
            status="completed",
            completed_at=self._now(),
        )

    def mark_awaiting_approval(self, job_id: str) -> None:
        """Mark a job as waiting for human repair approval."""

        self._update_status(
            job_id=job_id,
            status="awaiting_approval",
        )

    def mark_failed(
        self,
        job_id: str,
        error_message: str,
    ) -> None:
        self._update_status(
            job_id=job_id,
            status="failed",
            error_message=error_message,
            completed_at=self._now(),
        )

    def request_approval(
        self,
        job_id: str,
        reason: str,
        confidence: float,
    ) -> None:
        """Mark a job as waiting for human approval."""

        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE jobs
                SET
                    approval_status = ?,
                    approval_reason = ?,
                    approval_confidence = ?
                WHERE job_id = ?
                """,
                (
                    "pending",
                    reason,
                    confidence,
                    job_id,
                ),
            )

            connection.commit()
        finally:
            connection.close()

    def approve_job(self, job_id: str) -> None:
        """Mark a pending job as approved for repair."""

        self._update_approval_status(
            job_id=job_id,
            approval_status="approved",
        )

    def reject_job(self, job_id: str) -> None:
        """Mark a pending job as rejected."""

        self._update_approval_status(
            job_id=job_id,
            approval_status="rejected",
        )

    def get_job(
        self,
        job_id: str,
    ) -> dict | None:
        connection = get_connection()

        try:
            row = connection.execute(
                """
                SELECT
                    job_id,
                    repository,
                    commit_sha,
                    branch,
                    target_url,
                    status,
                    error_message,
                    created_at,
                    started_at,
                    completed_at,
                    approval_status,
                    approval_reason,
                    approval_confidence
                FROM jobs
                WHERE job_id = ?
                """,
                (job_id,),
            ).fetchone()
        finally:
            connection.close()

        if row is None:
            return None

        return dict(row)

    def get_all_jobs(self) -> list[dict]:
        connection = get_connection()

        try:
            rows = connection.execute(
                """
                SELECT
                    job_id,
                    repository,
                    commit_sha,
                    branch,
                    target_url,
                    status,
                    error_message,
                    created_at,
                    started_at,
                    completed_at,
                    approval_status,
                    approval_reason,
                    approval_confidence
                FROM jobs
                ORDER BY created_at DESC
                """
            ).fetchall()
        finally:
            connection.close()

        return [dict(row) for row in rows]

    def _update_status(
        self,
        job_id: str,
        status: str,
        error_message: str | None = None,
        started_at: str | None = None,
        completed_at: str | None = None,
    ) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE jobs
                SET
                    status = ?,
                    error_message = COALESCE(?, error_message),
                    started_at = COALESCE(?, started_at),
                    completed_at = COALESCE(?, completed_at)
                WHERE job_id = ?
                """,
                (
                    status,
                    error_message,
                    started_at,
                    completed_at,
                    job_id,
                ),
            )

            connection.commit()
        finally:
            connection.close()

    def _update_approval_status(
        self,
        job_id: str,
        approval_status: str,
    ) -> None:
        connection = get_connection()

        try:
            connection.execute(
                """
                UPDATE jobs
                SET approval_status = ?
                WHERE job_id = ?
                """,
                (
                    approval_status,
                    job_id,
                ),
            )

            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()


job_store = JobStore()
