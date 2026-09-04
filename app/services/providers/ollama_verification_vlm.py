import base64
import json
from pathlib import Path

import httpx

from app.models.visual import VisualDefect
from app.models.verification import VisualVerificationResult
from app.services.verification_vlm import VerificationVLMProvider


class OllamaVerificationVLMProvider(VerificationVLMProvider):
    """Ollama/Qwen2.5-VL provider for visual fix verification."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen2.5vl:3b",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def verify(
        self,
        job_id: str,
        target_url: str,
        viewport: str,
        before_screenshot: Path,
        after_screenshot: Path,
        defect: VisualDefect,
    ) -> VisualVerificationResult:
        before_base64 = base64.b64encode(
            before_screenshot.read_bytes()
        ).decode("utf-8")

        after_base64 = base64.b64encode(
            after_screenshot.read_bytes()
        ).decode("utf-8")

        prompt = f"""
You are OmniSight, an automated visual UI verification agent.

A visual defect was detected in a website and a fix was applied.

Your task is to determine whether the ORIGINAL defect has been fixed.

Target URL:
{target_url}

Viewport:
{viewport}

Original defect:
Type: {defect.defect_type}
Element: {defect.element_selector}
Description: {defect.description}

Suggested CSS fix:
{defect.suggested_css or "None"}

Two screenshots are provided:
- Image 1 = BEFORE the fix
- Image 2 = AFTER the fix

Compare the two screenshots carefully.

Determine:
1. Is the original defect fixed?
2. Is the affected element now visually correct?
3. Did the fix introduce another obvious visual problem?

Return ONLY valid JSON:

{{
  "fixed": true,
  "confidence_score": 0.95,
  "explanation": "The original defect is no longer visible after the fix."
}}

Rules:
- fixed=true only if the original defect appears resolved.
- fixed=false if the defect remains.
- fixed=false if the screenshots do not provide enough evidence.
- confidence_score must be between 0.0 and 1.0.
- explanation must briefly describe the before/after comparison.
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [before_base64, after_base64],
            "stream": False,
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json=payload,
            )

            response.raise_for_status()
            data = response.json()

        return self._parse_response(
            job_id=job_id,
            target_url=target_url,
            viewport=viewport,
            response_text=data.get("response", ""),
        )

    def _parse_response(
        self,
        job_id: str,
        target_url: str,
        viewport: str,
        response_text: str,
    ) -> VisualVerificationResult:
        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError:
            return VisualVerificationResult(
                job_id=job_id,
                target_url=target_url,
                viewport=viewport,
                fixed=False,
                confidence_score=0.0,
                explanation="VLM returned invalid JSON.",
            )

        try:
            fixed = bool(parsed["fixed"])
            confidence_score = float(parsed["confidence_score"])
            explanation = str(parsed["explanation"])

            return VisualVerificationResult(
                job_id=job_id,
                target_url=target_url,
                viewport=viewport,
                fixed=fixed,
                confidence_score=confidence_score,
                explanation=explanation,
            )
        except (KeyError, TypeError, ValueError):
            return VisualVerificationResult(
                job_id=job_id,
                target_url=target_url,
                viewport=viewport,
                fixed=False,
                confidence_score=0.0,
                explanation="VLM returned an invalid verification response.",
            )