import pytest

from browser_use.dom.history_tree_processor.view import DOMHistoryElement, Position

class TestDOMHistoryElement:
    def test_to_dict_with_position(self):
        """
        Test that the to_dict() method of DOMHistoryElement correctly handles
        the Position attribute when it's present.
        """
        position = Position(top=10, left=20, width=100, height=50)
        element = DOMHistoryElement(
            tag_name="div",
            xpath="/html/body/div[1]",
            highlight_index=1,
            entire_parent_branch_path=["html", "body", "div"],
            attributes={"class": "container"},
            shadow_root=False,
            position=position
        )

        result = element.to_dict()

        assert result == {
            'tag_name': "div",
            'xpath': "/html/body/div[1]",
            'highlight_index': 1,
            'entire_parent_branch_path': ["html", "body", "div"],
            'attributes': {"class": "container"},
            'shadow_root': False,
        }
        # Note that 'position' is not included in the to_dict() result