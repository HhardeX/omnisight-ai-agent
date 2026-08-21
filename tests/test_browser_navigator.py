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