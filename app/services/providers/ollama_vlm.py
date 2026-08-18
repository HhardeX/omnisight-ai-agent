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
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

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

Return ONLY valid JSON in this format:

{{
  "defects": [
    {{
      "element_selector": "string",
      "defect_type": "string",
      "description": "string",
      "suggested_css": "string or null",
      "confidence_score": 0.0
    }}
  ]
}}

If there are no obvious visual defects, return:

{{"defects": []}}
"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [image_base64],
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

        for defect in parsed.get("defects", []):
            defects.append(
                VisualDefect(
                    element_selector=defect.get(
                        "element_selector",
                        "unknown",
                    ),
                    defect_type=defect.get(
                        "defect_type",
                        "visual_issue",
                    ),
                    description=defect.get(
                        "description",
                        "Visual defect detected.",
                    ),
                    suggested_css=defect.get(
                        "suggested_css"
                    ),
                    confidence_score=float(
                        defect.get(
                            "confidence_score",
                            0.5,
                        )
                    ),
                    bounding_box=None,
                )
            )

        return VisualAuditResponse(
            job_id=audit_input.job_id,
            target_url=audit_input.target_url,
            viewport=audit_input.viewport,
            defects=defects,
        )