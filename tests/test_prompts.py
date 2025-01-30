import pytest

from browser_use.agent.prompts import AgentMessagePrompt, SystemPrompt
from browser_use.agent.views import AgentStepInfo
from browser_use.browser.views import BrowserState
from datetime import datetime
from unittest.mock import MagicMock

class TestSystemPrompt:
    def test_get_system_message_includes_current_date(self):
        """
        Test that the system message from SystemPrompt includes the current date and time.
        """
        # Arrange
        test_date = datetime(2023, 1, 1, 12, 0)
        action_description = "Test action description"
        system_prompt = SystemPrompt(action_description, test_date)

        # Act
        system_message = system_prompt.get_system_message()

        # Assert
        expected_date_string = "Current date and time: 2023-01-01 12:00"
        assert expected_date_string in system_message.content
        assert action_description in system_message.content