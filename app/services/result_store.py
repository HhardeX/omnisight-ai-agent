from app.models.audit import BrowserAuditResult
from app.models.jobs import BuildEvent
from app.models.visual import VisualAuditResponse


class AuditResultStore:
    """Simple in-memory store for completed OmniSight audits."""

    def __init__(self) -> None:
        self._browser_results: dict[str, BrowserAuditResult] = {}
        self._visual_results: dict[str, VisualAuditResponse] = {}
        self._build_events: dict[str, BuildEvent] = {}

    def save_build_event(
        self,
        job_id: str,
        build_event: BuildEvent,
    ) -> None:
        self._build_events[job_id] = build_event

    def get_build_event(
        self,
        job_id: str,
    ) -> BuildEvent | None:
        return self._build_events.get(job_id)

    def get_all_build_events(
        self,
    ) -> dict[str, BuildEvent]:
        return dict(self._build_events)

    def save(
        self,
        browser_result: BrowserAuditResult,
        visual_result: VisualAuditResponse,
    ) -> None:
        browser_key = f"{browser_result.job_id}-{browser_result.viewport}"
        visual_key = f"{visual_result.job_id}-{browser_result.viewport}"

        self._browser_results[browser_key] = browser_result
        self._visual_results[visual_key] = visual_result

    def get_browser_result(self, job_id: str) -> BrowserAuditResult | None:
        for result in self._browser_results.values():
            if result.job_id == job_id:
                return result
        return None

    def get_visual_result(self, job_id: str) -> VisualAuditResponse | None:
        for result in self._visual_results.values():
            if result.job_id == job_id:
                return result
        return None

    def get_all_browser_results(self) -> list[BrowserAuditResult]:
        return list(self._browser_results.values())

    def get_all_visual_results(self) -> list[VisualAuditResponse]:
        return list(self._visual_results.values())


result_store = AuditResultStore()