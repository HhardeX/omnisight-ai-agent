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


class FakePage:
    def __init__(self):
        self.injected_css = None

    async def add_style_tag(self, *, content):
        self.injected_css = content


@pytest.mark.asyncio
async def test_inject_css_adds_style_tag():
    manager = BrowserManager()
    fake_page = FakePage()
    manager._page = fake_page

    css = "#login { margin-top: 8px; }"

    await manager.inject_css(css)

    assert fake_page.injected_css == css


@pytest.mark.asyncio
async def test_inject_css_rejects_empty_css():
    manager = BrowserManager()
    manager._page = FakePage()

    with pytest.raises(ValueError, match="CSS cannot be empty."):
        await manager.inject_css("   ")
