from app.browser.navigator import BrowserManager
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.browser.navigator import BrowserManager


def test_browser_manager_has_required_responsive_viewports():
    assert set(BrowserManager.VIEWPORTS) == {
        "mobile",
        "tablet",
        "desktop",
    }


def test_mobile_viewport_dimensions():
    viewport = BrowserManager.VIEWPORTS["mobile"]

    assert viewport.width == 375
    assert viewport.height == 812


def test_tablet_viewport_dimensions():
    viewport = BrowserManager.VIEWPORTS["tablet"]

    assert viewport.width == 768
    assert viewport.height == 1024


def test_desktop_viewport_dimensions():
    viewport = BrowserManager.VIEWPORTS["desktop"]

    assert viewport.width == 1920
    assert viewport.height == 1080
@pytest.mark.asyncio
async def test_apply_css_injects_stylesheet():
    manager = BrowserManager()

    page = MagicMock()
    page.add_style_tag = AsyncMock()

    manager._page = page

    await manager.apply_css(
        ".button { margin-top: 8px; }"
    )

    page.add_style_tag.assert_awaited_once_with(
        content=".button { margin-top: 8px; }"
    )


@pytest.mark.asyncio
async def test_apply_css_rejects_empty_css():
    manager = BrowserManager()

    page = MagicMock()
    manager._page = page

    with pytest.raises(
        ValueError,
        match="CSS cannot be empty",
    ):
        await manager.apply_css("   ")


@pytest.mark.asyncio
async def test_apply_css_requires_started_browser():
    manager = BrowserManager()

    with pytest.raises(
        RuntimeError,
        match="BrowserManager has not been started",
    ):
        await manager.apply_css(
            ".button { margin-top: 8px; }"
        )
import pytest
from app.browser.navigator import BrowserManager


def test_browser_manager_has_required_responsive_viewports():
    assert set(BrowserManager.VIEWPORTS) == {
        "mobile",
        "tablet",
        "desktop",
    }


def test_mobile_viewport_dimensions():
    viewport = BrowserManager.VIEWPORTS["mobile"]

    assert viewport.width == 375
    assert viewport.height == 812


def test_tablet_viewport_dimensions():
    viewport = BrowserManager.VIEWPORTS["tablet"]

    assert viewport.width == 768
    assert viewport.height == 1024


def test_desktop_viewport_dimensions():
    viewport = BrowserManager.VIEWPORTS["desktop"]

    assert viewport.width == 1920
    assert viewport.height == 1080


@pytest.mark.asyncio
async def test_apply_css_requires_started_browser():
    manager = BrowserManager()

    with pytest.raises(RuntimeError):
        await manager.apply_css(
            "h1 { color: red; }"
        )