from app.models.audit import BrowserAuditResult
from app.models.visual import VisualAuditResponse


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


result_store = AuditResultStore()