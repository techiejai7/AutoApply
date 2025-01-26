import pytest

from browser_use.controller.views import SearchGoogleAction

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