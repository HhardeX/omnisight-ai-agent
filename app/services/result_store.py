from dataclasses import dataclass
import json

from app.db.database import get_connection
from app.models.audit import BrowserAuditResult
from app.models.visual import VisualAuditResponse


@dataclass(frozen=True, slots=True)
class PublishedRepair:
    """Published repair metadata shown by the QA dashboard."""

    job_id: str
    viewport: str
    branch_name: str
    commit_sha: str
    pull_request_url: str


class AuditResultStore:
    """Stores OmniSight audit results with optional SQLite persistence."""

    def __init__(self, persistent: bool = False) -> None:
        self._persistent = persistent

        self._browser_results: dict[
            tuple[str, str],
            BrowserAuditResult,
        ] = {}

        self._visual_results: dict[
            tuple[str, str],
            VisualAuditResponse,
        ] = {}

        self._published_repairs: dict[
            tuple[str, str],
            PublishedRepair,
        ] = {}

    def save(
        self,
        browser_result: BrowserAuditResult,
        visual_result: VisualAuditResponse,
    ) -> None:
        if self._persistent:
            connection = get_connection()

            try:
                connection.execute(
                    """
                    INSERT OR REPLACE INTO browser_results (
                        job_id,
                        target_url,
                        viewport,
                        screenshot_path,
                        dom_snapshot,
                        element_bounds
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        browser_result.job_id,
                        browser_result.target_url,
                        browser_result.viewport,
                        str(browser_result.screenshot_path),
                        browser_result.dom_snapshot,
                        json.dumps(
                            {
                                key: value.model_dump()
                                for key, value
                                in browser_result.element_bounds.items()
                            }
                        ),
                    ),
                )

                connection.execute(
                    """
                    INSERT OR REPLACE INTO visual_results (
                        job_id,
                        target_url,
                        viewport,
                        defects
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        visual_result.job_id,
                        visual_result.target_url,
                        visual_result.viewport,
                        visual_result.model_dump_json(),
                    ),
                )

                connection.commit()
            finally:
                connection.close()

            return

        key = (
            browser_result.job_id,
            browser_result.viewport,
        )

        self._browser_results[key] = browser_result
        self._visual_results[key] = visual_result

    def get_browser_result(
        self,
        job_id: str,
    ) -> BrowserAuditResult | None:
        if self._persistent:
            results = self.get_all_browser_results()
            results = [
                result
                for result in results
                if result.job_id == job_id
            ]

            return results[-1] if results else None

        results = [
            result
            for (stored_job_id, _), result
            in self._browser_results.items()
            if stored_job_id == job_id
        ]

        return results[-1] if results else None

    def get_visual_result(
        self,
        job_id: str,
    ) -> VisualAuditResponse | None:
        if self._persistent:
            results = self.get_all_visual_results()
            results = [
                result
                for result in results
                if result.job_id == job_id
            ]

            return results[-1] if results else None

        results = [
            result
            for (stored_job_id, _), result
            in self._visual_results.items()
            if stored_job_id == job_id
        ]

        return results[-1] if results else None

    def get_all_browser_results(
        self,
    ) -> list[BrowserAuditResult]:
        if self._persistent:
            connection = get_connection()

            try:
                rows = connection.execute(
                    """
                    SELECT
                        job_id,
                        target_url,
                        viewport,
                        screenshot_path,
                        dom_snapshot,
                        element_bounds
                    FROM browser_results
                    ORDER BY rowid
                    """
                ).fetchall()
            finally:
                connection.close()

            return [
                BrowserAuditResult(
                    job_id=row["job_id"],
                    target_url=row["target_url"],
                    viewport=row["viewport"],
                    screenshot_path=row["screenshot_path"],
                    dom_snapshot=row["dom_snapshot"],
                    element_bounds={
                        key: value
                        for key, value in json.loads(
                            row["element_bounds"]
                        ).items()
                    },
                )
                for row in rows
            ]

        return list(self._browser_results.values())

    def get_all_visual_results(
        self,
    ) -> list[VisualAuditResponse]:
        if self._persistent:
            connection = get_connection()

            try:
                rows = connection.execute(
                    """
                    SELECT defects
                    FROM visual_results
                    ORDER BY rowid
                    """
                ).fetchall()
            finally:
                connection.close()

            return [
                VisualAuditResponse.model_validate_json(
                    row["defects"]
                )
                for row in rows
            ]

        return list(self._visual_results.values())

    def save_published_repair(
        self,
        repair: PublishedRepair,
    ) -> None:
        if self._persistent:
            connection = get_connection()

            try:
                connection.execute(
                    """
                    INSERT OR REPLACE INTO published_repairs (
                        job_id,
                        viewport,
                        branch_name,
                        commit_sha,
                        pull_request_url
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        repair.job_id,
                        repair.viewport,
                        repair.branch_name,
                        repair.commit_sha,
                        repair.pull_request_url,
                    ),
                )

                connection.commit()
            finally:
                connection.close()

            return

        key = (
            repair.job_id,
            repair.viewport,
        )

        self._published_repairs[key] = repair

    def get_all_published_repairs(
        self,
    ) -> list[PublishedRepair]:
        if self._persistent:
            connection = get_connection()

            try:
                rows = connection.execute(
                    """
                    SELECT
                        job_id,
                        viewport,
                        branch_name,
                        commit_sha,
                        pull_request_url
                    FROM published_repairs
                    ORDER BY rowid
                    """
                ).fetchall()
            finally:
                connection.close()

            return [
                PublishedRepair(
                    job_id=row["job_id"],
                    viewport=row["viewport"],
                    branch_name=row["branch_name"],
                    commit_sha=row["commit_sha"],
                    pull_request_url=row["pull_request_url"],
                )
                for row in rows
            ]

        return list(self._published_repairs.values())


result_store = AuditResultStore(persistent=True)