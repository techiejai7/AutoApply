import asyncio
import pytest

from browser_use.browser.context import BrowserContext, BrowserContextConfig
from browser_use.browser.views import BrowserState
from unittest.mock import AsyncMock, MagicMock, patch

class TestBrowserContext:
    @pytest.mark.asyncio
    async def test_get_state(self):
        """
        Test the get_state method of BrowserContext.
        This test checks if the method correctly updates and returns the browser state.
        """
        # Mock the Browser class
        mock_browser = MagicMock()
        mock_browser.get_playwright_browser.return_value = AsyncMock()

        # Create a BrowserContextConfig
        config = BrowserContextConfig()

        # Create a BrowserContext instance
        context = BrowserContext(mock_browser, config)

        # Mock the _wait_for_page_and_frames_load method
        context._wait_for_page_and_frames_load = AsyncMock()

        # Mock the _update_state method
        mock_state = BrowserState(
            element_tree=MagicMock(),
            selector_map={},
            url="https://example.com",
            title="Example Page",
            tabs=[],
            screenshot="mock_screenshot",
            pixels_above=0,
            pixels_below=100
        )
        context._update_state = AsyncMock(return_value=mock_state)

        # Mock the save_cookies method
        context.save_cookies = AsyncMock()

        # Mock the get_session method
        mock_session = MagicMock()
        context.get_session = AsyncMock(return_value=mock_session)

        # Call the get_state method
        result = await context.get_state()

        # Assert that _wait_for_page_and_frames_load was called
        context._wait_for_page_and_frames_load.assert_called_once()

        # Assert that _update_state was called
        context._update_state.assert_called_once()

        # Assert that save_cookies was called if cookies_file is set
        if config.cookies_file:
            context.save_cookies.assert_called_once()
        else:
            context.save_cookies.assert_not_called()

        # Assert that the returned state matches the mock state
        assert result == mock_state

        # Assert that the cached_state in the session was updated
        assert mock_session.cached_state == mock_state