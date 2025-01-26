import pytest

from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from unittest.mock import MagicMock, patch
from urllib.parse import urlparse

class TestBrowserContext:
    """Test class for BrowserContext"""

    @pytest.fixture
    def mock_browser(self):
        return MagicMock(spec=Browser)

    @patch('browser_use.browser.context.uuid.uuid4')
    def test_browser_context_initialization(self, mock_uuid, mock_browser):
        """
        Test the initialization of BrowserContext with custom configuration.
        This test checks if:
        1. The context_id is set correctly
        2. The config is set correctly
        3. The browser attribute is set correctly
        4. The session is initially set to None
        """
        # Arrange
        mock_uuid.return_value = "test-uuid"
        custom_config = BrowserContextConfig(
            cookies_file="test_cookies.json",
            minimum_wait_page_load_time=1.0,
            browser_window_size={'width': 1920, 'height': 1080},
            highlight_elements=False
        )

        # Act
        context = BrowserContext(mock_browser, config=custom_config)

        # Assert
        assert context.context_id == "test-uuid"
        assert context.config == custom_config
        assert context.browser == mock_browser
        assert context.session is None

        # Check if specific config values are set correctly
        assert context.config.cookies_file == "test_cookies.json"
        assert context.config.minimum_wait_page_load_time == 1.0
        assert context.config.browser_window_size == {'width': 1920, 'height': 1080}
        assert context.config.highlight_elements is False

    @pytest.mark.parametrize("url, allowed_domains, expected", [
        ("https://example.com", ["example.com"], True),
        ("https://subdomain.example.com", ["example.com"], True),
        ("https://another-domain.com", ["example.com"], False),
        ("https://example.com:8080", ["example.com"], True),
        ("http://example.com", None, True),
        ("https://malicious.com", ["example.com", "safe.com"], False),
    ])
    def test_is_url_allowed(self, mock_browser, url, allowed_domains, expected):
        """
        Test the _is_url_allowed method of BrowserContext.
        This test checks if:
        1. URLs matching the allowed domains are correctly identified as allowed
        2. URLs not matching the allowed domains are correctly identified as not allowed
        3. Subdomains of allowed domains are correctly identified as allowed
        4. URLs with ports are correctly handled
        5. All URLs are allowed when no allowed_domains are specified
        6. Multiple allowed domains are correctly handled
        """
        # Arrange
        config = BrowserContextConfig(allowed_domains=allowed_domains)
        context = BrowserContext(mock_browser, config=config)

        # Act
        result = context._is_url_allowed(url)

        # Assert
        assert result == expected, f"Expected {expected} for URL {url} with allowed domains {allowed_domains}"

    """Test class for BrowserContext"""

    @pytest.fixture
    def mock_browser(self):
        return MagicMock()

    @pytest.mark.parametrize("xpath, expected_css", [
        ("/html/body/div", "html > body > div"),
        ("/html/body/div[1]", "html > body > div:nth-of-type(1)"),
        ("/html/body/div[last()]", "html > body > div:last-of-type"),
        ("/html/body/div[position()>1]", "html > body > div:nth-of-type(n+2)"),
        ("/html/body/div[@class='test']", "html > body > div"),
        ("/html/body/div[@id='main']", "html > body > div"),
    ])
    def test_convert_simple_xpath_to_css_selector(self, mock_browser, xpath, expected_css):
        """
        Test the _convert_simple_xpath_to_css_selector method of BrowserContext.
        This test checks if:
        1. Simple XPath expressions are correctly converted to CSS selectors
        2. XPath expressions with indices are correctly handled
        3. XPath expressions with last() function are correctly converted
        4. XPath expressions with position() function are correctly converted
        5. XPath expressions with class attributes are converted without the class
        6. XPath expressions with id attributes are converted without the id
        """
        # Arrange
        context = BrowserContext(mock_browser)

        # Act
        result = context._convert_simple_xpath_to_css_selector(xpath)

        # Assert
        assert result == expected_css, f"Expected '{expected_css}' for XPath '{xpath}', but got '{result}'"

@pytest.mark.parametrize("xpath, expected_css", [
    ("/html/body/div", "html > body > div"),
    ("/html/body/div[1]", "html > body > div:nth-of-type(1)"),
    ("/html/body/div[last()]", "html > body > div:last-of-type"),
    ("/html/body/div[position()>1]", "html > body > div:nth-of-type(n+2)"),
    ("/html/body/div[@class='test']", "html > body > div"),
    ("/html/body/div[@id='main']", "html > body > div"),
])
def test_convert_simple_xpath_to_css_selector(self, mock_browser, xpath, expected_css):
    """
    Test the _convert_simple_xpath_to_css_selector method of BrowserContext.
    This test checks if:
    1. Simple XPath expressions are correctly converted to CSS selectors
    2. XPath expressions with indices are correctly handled
    3. XPath expressions with last() function are correctly converted
    4. XPath expressions with position() function are correctly converted
    5. XPath expressions with class attributes are converted without the class
    6. XPath expressions with id attributes are converted without the id
    """
    # Arrange
    context = BrowserContext(mock_browser)

    # Act
    result = context._convert_simple_xpath_to_css_selector(xpath)

    # Assert
    assert result == expected_css, f"Expected '{expected_css}' for XPath '{xpath}', but got '{result}'"