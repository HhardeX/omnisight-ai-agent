from pathlib import Path

import pytest

from app.models.visual import VisualAuditInput
from app.services.providers.rule_based_vlm import RuleBasedVLMProvider


@pytest.mark.asyncio
async def test_rule_based_provider_accepts_existing_screenshot(
    tmp_path: Path,
) -> None:
    screenshot = tmp_path / "capture.png"
    screenshot.write_bytes(b"fake-image-data")

    audit_input = VisualAuditInput(
        job_id="job-1",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=str(screenshot),
        dom_snapshot="<html><body><h1>Hello</h1></body></html>",
    )

    provider = RuleBasedVLMProvider()

    result = await provider.analyze(audit_input)

    assert result.job_id == "job-1"
    assert result.target_url == "https://example.com"
    assert result.viewport == "desktop"
    assert result.defect_count == 0


@pytest.mark.asyncio
async def test_rule_based_provider_rejects_missing_screenshot(
    tmp_path: Path,
) -> None:
    screenshot = tmp_path / "missing.png"

    audit_input = VisualAuditInput(
        job_id="job-2",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=str(screenshot),
        dom_snapshot="<html></html>",
    )

    provider = RuleBasedVLMProvider()

    with pytest.raises(FileNotFoundError):
        await provider.analyze(audit_input)


@pytest.mark.asyncio
async def test_rule_based_provider_detects_missing_dom(
    tmp_path: Path,
) -> None:
    screenshot = tmp_path / "capture.png"
    screenshot.write_bytes(b"fake-image-data")

    audit_input = VisualAuditInput(
        job_id="job-3",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=str(screenshot),
        dom_snapshot="   ",
    )

    provider = RuleBasedVLMProvider()

    result = await provider.analyze(audit_input)

    assert result.defect_count == 1
    assert result.defects[0].element_selector == "html"
    assert result.defects[0].defect_type == "missing_dom"
    assert result.defects[0].confidence_score == 1.0


@pytest.mark.asyncio
async def test_rule_based_provider_detects_missing_h1(
    tmp_path: Path,
) -> None:
    screenshot = tmp_path / "capture.png"
    screenshot.write_bytes(b"fake-image-data")

    audit_input = VisualAuditInput(
        job_id="job-4",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=str(screenshot),
        dom_snapshot="<html><body><p>Hello</p></body></html>",
    )

    provider = RuleBasedVLMProvider()

    result = await provider.analyze(audit_input)

    assert result.defect_count == 1
    assert result.defects[0].element_selector == "h1"
    assert result.defects[0].defect_type == "missing_h1"
    assert result.defects[0].confidence_score == 0.95