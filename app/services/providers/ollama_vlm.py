
import base64
import json
from pathlib import Path

import httpx

from app.models.visual import (
    VisualAuditInput,
    VisualAuditResponse,
    VisualDefect,
)
from app.services.vlm import VLMProvider


class OllamaVLMProvider(VLMProvider):
    """Local VLM provider using Ollama and Qwen2.5-VL."""

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "qwen2.5vl:3b",
        timeout: float = 900.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def analyze(
        self,
        audit_input: VisualAuditInput,
    ) -> VisualAuditResponse:
        screenshot = Path(audit_input.screenshot_path)

        if not screenshot.is_file():
            raise FileNotFoundError(
                f"Screenshot not found: {screenshot}"
            )

        image_base64 = base64.b64encode(
            screenshot.read_bytes()
        ).decode("utf-8")

        prompt = f"""
You are OmniSight, an automated visual UI auditing agent.

Analyze the provided website screenshot.

Target URL:
{audit_input.target_url}

Viewport:
{audit_input.viewport}

DOM snapshot:
{audit_input.dom_snapshot[:12000]}

Identify visible UI defects such as:
- broken or missing UI elements
- layout problems
- overlapping elements
- incorrect alignment
- unreadable text
- suspicious spacing
- visual rendering problems
- missing important elements

Return ONLY valid JSON in exactly this structure:

{{
  "defects": [
    {{
      "element_selector": "actual CSS selector or DOM element",
      "defect_type": "actual defect category",
      "description": "specific explanation of the visible defect",
      "suggested_css": "specific CSS fix or null",
      "confidence_score": 0.0
    }}
  ]
}}

IMPORTANT:
- Do NOT return placeholder values such as "string", "actual CSS selector or DOM element", or "actual defect category".
- Do NOT invent a defect merely to fill the schema.
- Only report defects that are visibly supported by the screenshot.
- Use the DOM snapshot to help identify the actual element selector.
- If no real visible defect can be identified, return exactly:
{{"defects":[]}}
- confidence_score must be between 0.0 and 1.0.
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False,
            "format": "json",
        }

        print(
            f"[OmniSight] Starting VLM analysis "
            f"for {audit_input.viewport} "
            f"using {self.model}"
        )

        timeout = httpx.Timeout(
            connect=30.0,
            read=self.timeout,
            write=60.0,
            pool=30.0,
        )

        try:
            async with httpx.AsyncClient(
                timeout=timeout
            ) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

        except httpx.ReadTimeout as exc:
            print(
                f"[OmniSight] Ollama VLM read timeout "
                f"for {audit_input.viewport} "
                f"after {self.timeout} seconds"
            )
            raise exc

        print(
            f"[OmniSight] VLM analysis completed "
            f"for {audit_input.viewport}"
        )

        return self._parse_response(
            audit_input,
            data.get("response", ""),
        )

    def _parse_response(
        self,
        audit_input: VisualAuditInput,
        response_text: str,
    ) -> VisualAuditResponse:
        try:
            parsed = json.loads(response_text)
        except json.JSONDecodeError:
            return VisualAuditResponse(
                job_id=audit_input.job_id,
                target_url=audit_input.target_url,
                viewport=audit_input.viewport,
            )

        defects: list[VisualDefect] = []

        placeholder_values = {
            "string",
            "actual css selector or dom element",
            "actual defect category",
            "specific explanation of the visible defect",
            "specific css fix or null",
        }

        for defect in parsed.get("defects", []):
            element_selector = defect.get(
                "element_selector",
                "unknown",
            )
            defect_type = defect.get(
                "defect_type",
                "visual_issue",
            )
            description = defect.get(
                "description",
                "Visual defect detected.",
            )

            normalized_values = {
                str(element_selector).strip().lower(),
                str(defect_type).strip().lower(),
                str(description).strip().lower(),
            }

            if normalized_values & placeholder_values:
                continue

            confidence_score = float(
                defect.get(
                    "confidence_score",
                    0.5,
                )
            )

            confidence_score = max(
                0.0,
                min(1.0, confidence_score),
            )

            defects.append(
                VisualDefect(
                    element_selector=element_selector,
                    defect_type=defect_type,
                    description=description,
                    suggested_css=defect.get(
                        "suggested_css"
                    ),
                    confidence_score=confidence_score,
                    bounding_box=None,
                )
            )

        return VisualAuditResponse(
            job_id=audit_input.job_id,
            target_url=audit_input.target_url,
            viewport=audit_input.viewport,
            defects=defects,
        )

