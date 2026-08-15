from app.models.audit import BrowserAuditResult
from app.models.visual import VisualAuditResponse


class AuditResultStore:
    """Simple in-memory store for completed OmniSight audits."""

    def __init__(self) -> None:
        self._browser_results: dict[str, BrowserAuditResult] = {}
        self._visual_results: dict[str, VisualAuditResponse] = {}

    def save(
        self,
        browser_result: BrowserAuditResult,
        visual_result: VisualAuditResponse,
    ) -> None:
        self._browser_results[browser_result.job_id] = browser_result
        self._visual_results[visual_result.job_id] = visual_result

    def get_browser_result(self, job_id: str) -> BrowserAuditResult | None:
        return self._browser_results.get(job_id)

    def get_visual_result(self, job_id: str) -> VisualAuditResponse | None:
        return self._visual_results.get(job_id)

    def get_all_browser_results(self) -> list[BrowserAuditResult]:
        return list(self._browser_results.values())

    def get_all_visual_results(self) -> list[VisualAuditResponse]:
        return list(self._visual_results.values())


result_store = AuditResultStore()