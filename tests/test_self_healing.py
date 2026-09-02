from app.models.visual import VisualAuditResponse, VisualDefect
from app.services.self_healing import SelfHealingService


def test_self_healing_collects_css_fixes() -> None:
    result = VisualAuditResponse(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        defects=[
            VisualDefect(
                element_selector="#login",
                defect_type="spacing",
                description="Login button has incorrect spacing.",
                suggested_css="  margin-top: 8px;  ",
                confidence_score=0.95,
            ),
        ],
    )

    fixes = SelfHealingService().collect_fixes(result)

    assert len(fixes) == 1
    assert fixes[0].element_selector == "#login"
    assert fixes[0].suggested_css == "margin-top: 8px;"


def test_self_healing_ignores_defects_without_css() -> None:
    result = VisualAuditResponse(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        defects=[
            VisualDefect(
                element_selector="#header",
                defect_type="layout",
                description="Header layout is incorrect.",
                suggested_css=None,
                confidence_score=0.80,
            ),
            VisualDefect(
                element_selector="#footer",
                defect_type="layout",
                description="Footer layout is incorrect.",
                suggested_css="   ",
                confidence_score=0.80,
            ),
        ],
    )

    fixes = SelfHealingService().collect_fixes(result)

    assert fixes == []
