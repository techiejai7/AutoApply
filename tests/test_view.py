import pytest

from browser_use.dom.history_tree_processor.view import DOMHistoryElement

class TestDOMHistoryElement:
    """Test class for DOMHistoryElement"""

    def test_to_dict_method(self):
        """
        Test the to_dict method of DOMHistoryElement.
        This test ensures that the to_dict method correctly converts
        the DOMHistoryElement object to a dictionary with all its attributes.
        """
        # Create a sample DOMHistoryElement
        dom_element = DOMHistoryElement(
            tag_name="div",
            xpath="/html/body/div[1]",
            highlight_index=1,
            entire_parent_branch_path=["html", "body", "div"],
            attributes={"class": "container", "id": "main"},
            shadow_root=False
        )

        # Call the to_dict method
        result = dom_element.to_dict()

        # Assert that the result is a dictionary
        assert isinstance(result, dict)

        # Assert that all expected keys are present in the dictionary
        expected_keys = ['tag_name', 'xpath', 'highlight_index', 'entire_parent_branch_path', 'attributes', 'shadow_root']
        assert all(key in result for key in expected_keys)

        # Assert that the values in the dictionary match the original object's attributes
        assert result['tag_name'] == "div"
        assert result['xpath'] == "/html/body/div[1]"
        assert result['highlight_index'] == 1
        assert result['entire_parent_branch_path'] == ["html", "body", "div"]
        assert result['attributes'] == {"class": "container", "id": "main"}
        assert result['shadow_root'] == False