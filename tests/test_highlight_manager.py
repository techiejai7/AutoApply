import pytest

from PIL import Image
from browser_use.browser.manager.highlight_manager import HighlightManager
from unittest.mock import Mock

class TestHighlightManager:
    def test_highlight_element_with_empty_list(self):
        """
        Test that highlight_element method handles an empty list of elements without errors.
        This ensures the method is robust against edge cases where no elements are provided.
        """
        # Arrange
        highlight_manager = HighlightManager()
        mock_image = Image.new('RGB', (100, 100))  # Create a mock image
        empty_element_list = []

        # Act
        highlight_manager.highlight_element(empty_element_list, mock_image)

        # Assert
        # Since no exception is raised and no changes are made to the image,
        # we just assert that the method call completes successfully
        assert True  # If we reach this point, the test passes