
from dataclasses import dataclass
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
    """In-memory store for OmniSight audit results across all viewports."""

    def __init__(self) -> None:
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
        results = [
            result
            for (stored_job_id, _), result
            in self._browser_results.items()
            if stored_job_id == job_id
        ]

        if not results:
            return None

        return results[-1]

    def get_visual_result(
        self,
        job_id: str,
    ) -> VisualAuditResponse | None:
        results = [
            result
            for (stored_job_id, _), result
            in self._visual_results.items()
            if stored_job_id == job_id
        ]

        if not results:
            return None

        return results[-1]

    def get_all_browser_results(
        self,
    ) -> list[BrowserAuditResult]:
        return list(self._browser_results.values())

    def get_all_visual_results(
        self,
    ) -> list[VisualAuditResponse]:
        return list(self._visual_results.values())
    
    def save_published_repair(
        self,
        repair: PublishedRepair,
    ) -> None:
        """Store a successfully published repair."""

        key = (
            repair.job_id,
            repair.viewport,
        )

        self._published_repairs[key] = repair


    def get_all_published_repairs(
        self,
    ) -> list[PublishedRepair]:
        """Return all successfully published repairs."""

        return list(self._published_repairs.values())


result_store = AuditResultStore()