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


@pytest.mark.asyncio
async def test_screenshot_roi_captures_requested_region(tmp_path):
    manager = BrowserManager()

    page = MagicMock()
    page.screenshot = AsyncMock()

    manager._page = page

    output_path = tmp_path / "roi.png"

    result = await manager.screenshot_roi(
        output_path,
        x=10,
        y=20,
        width=300,
        height=200,
    )

    assert result == output_path

    page.screenshot.assert_awaited_once_with(
        path=str(output_path),
        full_page=False,
        clip={
            "x": 10,
            "y": 20,
            "width": 300,
            "height": 200,
        },
    )


@pytest.mark.asyncio
async def test_screenshot_roi_rejects_invalid_dimensions(tmp_path):
    manager = BrowserManager()

    page = MagicMock()
    page.screenshot = AsyncMock()

    manager._page = page

    with pytest.raises(
        ValueError,
        match="ROI width and height",
    ):
        await manager.screenshot_roi(
            tmp_path / "roi.png",
            x=0,
            y=0,
            width=0,
            height=200,
        )


@pytest.mark.asyncio
async def test_screenshot_roi_requires_started_browser(tmp_path):
    manager = BrowserManager()

    with pytest.raises(
        RuntimeError,
        match="BrowserManager has not been started",
    ):
        await manager.screenshot_roi(
            tmp_path / "roi.png",
            x=0,
            y=0,
            width=100,
            height=100,
        )


@pytest.mark.asyncio
async def test_screenshot_chunks_creates_vertical_chunks(tmp_path):
    manager = BrowserManager()

    page = MagicMock()
    page.evaluate = AsyncMock(
        return_value={
            "width": 800,
            "height": 1800,
            "viewportHeight": 600,
        }
    )
    page.screenshot = AsyncMock()

    manager._page = page

    output_directory = tmp_path / "chunks"

    chunks = await manager.screenshot_chunks(
        output_directory,
        chunk_height=600,
    )

    assert len(chunks) == 3

    assert chunks[0].name == "chunk-001.png"
    assert chunks[1].name == "chunk-002.png"
    assert chunks[2].name == "chunk-003.png"

    assert page.screenshot.await_count == 3

    expected_calls = [
        {
            "path": str(output_directory / "chunk-001.png"),
            "full_page": False,
            "clip": {
                "x": 0,
                "y": 0,
                "width": 800,
                "height": 600,
            },
        },
        {
            "path": str(output_directory / "chunk-002.png"),
            "full_page": False,
            "clip": {
                "x": 0,
                "y": 600,
                "width": 800,
                "height": 600,
            },
        },
        {
            "path": str(output_directory / "chunk-003.png"),
            "full_page": False,
            "clip": {
                "x": 0,
                "y": 1200,
                "width": 800,
                "height": 600,
            },
        },
    ]

    actual_calls = [
        call.kwargs
        for call in page.screenshot.await_args_list
    ]

    assert actual_calls == expected_calls


@pytest.mark.asyncio
async def test_screenshot_chunks_handles_final_partial_chunk(tmp_path):
    manager = BrowserManager()

    page = MagicMock()
    page.evaluate = AsyncMock(
        return_value={
            "width": 800,
            "height": 1500,
            "viewportHeight": 600,
        }
    )
    page.screenshot = AsyncMock()

    manager._page = page

    chunks = await manager.screenshot_chunks(
        tmp_path / "chunks",
        chunk_height=600,
    )

    assert len(chunks) == 3

    final_call = page.screenshot.await_args_list[-1]

    assert final_call.kwargs["clip"] == {
        "x": 0,
        "y": 1200,
        "width": 800,
        "height": 300,
    }


@pytest.mark.asyncio
async def test_screenshot_chunks_rejects_invalid_chunk_height(tmp_path):
    manager = BrowserManager()

    page = MagicMock()
    manager._page = page

    with pytest.raises(
        ValueError,
        match="chunk_height",
    ):
        await manager.screenshot_chunks(
            tmp_path / "chunks",
            chunk_height=0,
        )


@pytest.mark.asyncio
async def test_screenshot_chunks_requires_started_browser(tmp_path):
    manager = BrowserManager()

    with pytest.raises(
        RuntimeError,
        match="BrowserManager has not been started",
    ):
        await manager.screenshot_chunks(
            tmp_path / "chunks",
            chunk_height=600,
        )