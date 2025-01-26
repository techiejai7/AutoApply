import pytest

from browser_use.browser.views import BrowserStateHistory, TabInfo
from browser_use.controller.views import SearchGoogleAction
from browser_use.dom.history_tree_processor.service import DOMHistoryElement

class TestActionInputModels:
    """Test suite for Action Input Models in views.py"""

    def test_search_google_action_valid_query(self):
        """
        Test that SearchGoogleAction correctly handles a valid query string.
        This test ensures that the model can be instantiated with a valid query
        and that the query attribute is correctly set.
        """
        query = "pytest tutorial"
        action = SearchGoogleAction(query=query)
        assert action.query == query
        assert isinstance(action, SearchGoogleAction)

class TestBrowserStateHistory:
    """Test suite for BrowserStateHistory in views.py"""

    def test_browser_state_history_to_dict(self):
        """
        Test that BrowserStateHistory.to_dict() correctly converts the object to a dictionary.
        This test ensures that all attributes are properly serialized, including nested objects.
        """
        # Create a sample BrowserStateHistory object
        tabs = [TabInfo(page_id=1, url="https://example.com", title="Example")]
        interacted_element = [
            DOMHistoryElement(
                tag_name="div",
                attributes={"id": "button"},
                xpath="/html/body/div[1]",
                highlight_index=0,
                entire_parent_branch_path=["/html", "/html/body", "/html/body/div[1]"]
            ),
            None
        ]
        browser_state = BrowserStateHistory(
            url="https://example.com",
            title="Example Page",
            tabs=tabs,
            interacted_element=interacted_element,
            screenshot="base64_encoded_screenshot"
        )

        # Call the to_dict method
        result = browser_state.to_dict()

        # Assert that the result is a dictionary
        assert isinstance(result, dict)

        # Check that all expected keys are present
        expected_keys = ['tabs', 'screenshot', 'interacted_element', 'url', 'title']
        assert all(key in result for key in expected_keys)

        # Check that tabs are correctly serialized
        assert len(result['tabs']) == 1
        assert result['tabs'][0] == tabs[0].model_dump()

        # Check that interacted_element is correctly serialized
        assert len(result['interacted_element']) == 2
        assert result['interacted_element'][0] == interacted_element[0].to_dict()
        assert result['interacted_element'][1] is None

        # Check other attributes
        assert result['url'] == "https://example.com"
        assert result['title'] == "Example Page"
        assert result['screenshot'] == "base64_encoded_screenshot"