from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


@dataclass(frozen=True, slots=True)
class Viewport:
    name: str
    width: int
    height: int


class BrowserManager:
    """Manages Playwright browser lifecycle and page inspection."""

    VIEWPORTS: dict[str, Viewport] = {
        "mobile": Viewport("mobile", 375, 812),
        "tablet": Viewport("tablet", 768, 1024),
        "desktop": Viewport("desktop", 1920, 1080),
    }

    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    async def start(self, viewport: str = "desktop") -> Page:
        """Start Chromium and create a page with the requested viewport."""

        if viewport not in self.VIEWPORTS:
            available = ", ".join(self.VIEWPORTS)
            raise ValueError(
                f"Unknown viewport '{viewport}'. "
                f"Available viewports: {available}"
            )

        selected = self.VIEWPORTS[viewport]

        self._playwright = await async_playwright().start()

        try:
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless
            )

            self._context = await self._browser.new_context(
                viewport={
                    "width": selected.width,
                    "height": selected.height,
                }
            )

            self._page = await self._context.new_page()

            return self._page

        except Exception:
            await self.stop()
            raise

    async def navigate(
        self,
        url: str,
        wait_until: str = "networkidle",
    ) -> Page:
        """Navigate to a URL using the active Playwright page."""

        if self._page is None:
            raise RuntimeError(
                "BrowserManager has not been started. "
                "Call 'await start()' first."
            )

        await self._page.goto(
            url,
            wait_until=wait_until,
        )

        return self._page

    async def inject_css(
        self,
        css: str,
    ) -> None:
        """Inject CSS into the active page without changing source files."""

        if self._page is None:
            raise RuntimeError(
                "BrowserManager has not been started."
            )

        if not css.strip():
            raise ValueError("CSS cannot be empty.")

        await self._page.add_style_tag(
            content=css,
        )

    async def screenshot(
        self,
        output_path: str | Path,
        full_page: bool = True,
    ) -> Path:
        """Capture a screenshot of the current page."""

        if self._page is None:
            raise RuntimeError(
                "BrowserManager has not been started."
            )

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        await self._page.screenshot(
            path=str(path),
            full_page=full_page,
        )

        return path

    async def get_dom_snapshot(self) -> str:
        """Return the current page HTML."""

        if self._page is None:
            raise RuntimeError(
                "BrowserManager has not been started."
            )

        return await self._page.content()

    async def get_element_bounds(
        self,
        selector: str,
    ) -> dict[str, float] | None:
        """Return an element's bounding box."""

        if self._page is None:
            raise RuntimeError(
                "BrowserManager has not been started."
            )

        element = self._page.locator(selector).first

        if await element.count() == 0:
            return None

        box = await element.bounding_box()

        if box is None:
            return None

        return {
            "x": box["x"],
            "y": box["y"],
            "width": box["width"],
            "height": box["height"],
        }

    async def stop(self) -> None:
        """Safely close the browser and Playwright."""

        if self._context is not None:
            await self._context.close()
            self._context = None

        if self._browser is not None:
            await self._browser.close()
            self._browser = None

        if self._playwright is not None:
            await self._playwright.stop()
            self._playwright = None

        self._page = None

    async def __aenter__(self) -> "BrowserManager":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: Any,
    ) -> None:
        await self.stop()