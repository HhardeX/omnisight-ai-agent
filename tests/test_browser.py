import asyncio
from pathlib import Path

from app.browser.navigator import BrowserManager


async def main() -> None:
    output_dir = Path("artifacts")
    output_dir.mkdir(parents=True, exist_ok=True)

    async with BrowserManager(headless=True) as browser:
        page = await browser.start(viewport="desktop")

        await browser.navigate("https://example.com")

        title = await page.title()
        print(f"Page title: {title}")

        screenshot = await browser.screenshot(
            output_dir / "example-desktop.png"
        )
        print(f"Screenshot saved: {screenshot}")

        dom = await browser.get_dom_snapshot()
        print(f"DOM size: {len(dom)} characters")

        heading_bounds = await browser.get_element_bounds("h1")
        print(f"H1 bounds: {heading_bounds}")


if __name__ == "__main__":
    asyncio.run(main())