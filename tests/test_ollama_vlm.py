import asyncio
import base64
import json
from pathlib import Path

import pytest

from app.models.visual import VisualAuditInput
from app.services.providers.ollama_vlm import OllamaVLMProvider


def make_input(screenshot_path: str) -> VisualAuditInput:
    return VisualAuditInput(
        job_id="vlm-test-001",
        target_url="https://example.com",
        viewport="desktop",
        screenshot_path=screenshot_path,
        dom_snapshot="<html><body><h1>Example Domain</h1></body></html>",
    )


def test_ollama_provider_rejects_missing_screenshot() -> None:
    provider = OllamaVLMProvider()

    with pytest.raises(FileNotFoundError):
        asyncio.run(
            provider.analyze(
                make_input("artifacts/does-not-exist.png")
            )
        )


def test_ollama_provider_parses_valid_response() -> None:
    provider = OllamaVLMProvider()

    audit_input = make_input("artifacts/example-desktop.png")

    response_text = json.dumps(
        {
            "defects": [
                {
                    "element_selector": "#login",
                    "defect_type": "overlap",
                    "description": "Login button overlaps the form.",
                    "suggested_css": "margin-top: 8px;",
                    "confidence_score": 0.95,
                }
            ]
        }
    )

    result = provider._parse_response(
        audit_input,
        response_text,
    )

    assert result.job_id == "vlm-test-001"
    assert result.defect_count == 1
    assert result.defects[0].defect_type == "overlap"
    assert result.defects[0].confidence_score == 0.95


def test_ollama_provider_handles_invalid_json() -> None:
    provider = OllamaVLMProvider()

    audit_input = make_input("artifacts/example-desktop.png")

    result = provider._parse_response(
        audit_input,
        "not valid json",
    )

    assert result.job_id == "vlm-test-001"
    assert result.defect_count == 0