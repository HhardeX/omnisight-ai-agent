import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

from app.models.visual import VisualDefect
from app.services.visual_verification import VisualVerificationService
from app.services.providers.ollama_verification_vlm import OllamaVerificationVLMProvider


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
DEMO_PAGE = ARTIFACTS / "verification_demo.html"
BEFORE = ARTIFACTS / "verification_before.png"
AFTER = ARTIFACTS / "verification_after.png"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OmniSight Verification Demo</title>
    <style>
        body {
            margin: 0;
            padding: 60px;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }

        .card {
            width: 520px;
            margin: 0 auto;
            padding: 32px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.12);
        }

        h1 {
            margin-top: 0;
        }

        #submit-button {
            display: none;
            margin-top: 24px;
            padding: 12px 24px;
            border: 0;
            border-radius: 6px;
            background: #222;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }

        #submit-button.fixed {
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Checkout</h1>
        <p>Review your order before continuing.</p>
        <button id="submit-button">Submit Order</button>
    </div>
</body>
</html>
"""


async def main():
    ARTIFACTS.mkdir(exist_ok=True)
    DEMO_PAGE.write_text(HTML, encoding="utf-8")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page(
            viewport={"width": 1280, "height": 720}
        )

        await page.goto(DEMO_PAGE.as_uri())

        # BEFORE: submit button is deliberately hidden.
        await page.screenshot(path=str(BEFORE), full_page=True)

        # Simulate the self-healing action.
        await page.locator("#submit-button").evaluate(
            "(element) => element.classList.add('fixed')"
        )

        # AFTER: submit button is now visible.
        await page.screenshot(path=str(AFTER), full_page=True)

        await browser.close()

    defect = VisualDefect(
        element_selector="#submit-button",
        defect_type="visibility",
        description="The Submit Order button is hidden and not visible to the user.",
        suggested_css="display: inline-block;",
        confidence_score=0.98,
    )

    provider = OllamaVerificationVLMProvider()

    service = VisualVerificationService(provider)

    result = await service.verify(
        job_id="verification-demo-001",
        target_url=DEMO_PAGE.as_uri(),
        viewport="1280x720",
        before_screenshot_path=str(BEFORE),
        after_screenshot_path=str(AFTER),
        defect=defect,
    )

    print()
    print("=" * 60)
    print("OMNISIGHT POST-FIX VLM VERIFICATION")
    print("=" * 60)
    print(f"Before screenshot : {BEFORE}")
    print(f"After screenshot  : {AFTER}")
    print(f"Fixed             : {result.fixed}")
    print(f"Confidence        : {result.confidence_score}")
    print(f"Explanation       : {result.explanation}")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
