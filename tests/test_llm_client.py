import pytest
from unittest.mock import MagicMock
from src.lib.llm_client.llm_client import LlMClient
from src.types.schema import LlmMessage

class MockLlMClient(LlMClient):
    def _send_message_implementation_specific_logic(self, message: LlmMessage, **kwargs) -> LlmMessage:
        return LlmMessage(role='bot', content='Response to the message')

class TestResetMemory:
    def test_reset_memory(self):
        client = MockLlMClient()
        client._memory = [LlmMessage(role='user', content='test')]
        assert len(client._memory) > 0
        client.reset_memory()
        assert len(client._memory) == 0

class TestSendMessage:
    def test_send_message_add_to_memory_without_response(self):
        client = MockLlMClient()
        message = 'Hello, world!'
        client.send_message(message, add_to_memory_without_response=True)
        assert len(client._memory) == 1

    def test_send_message_updates_memory_with_response(self):
        client = MockLlMClient()
        mock_response = MagicMock(LlmMessage)
        mock_response.content = 'Response to the message'
        client._send_message_implementation_specific_logic = MagicMock(return_value=mock_response)
        client.send_message('Hello, world!')
        assert len(client._memory) == 2

    def test_send_message_expecting_json_response_valid_json(self):
        client = MockLlMClient()
        message = 'Give me a JSON response.'
        mock_response = MagicMock(LlmMessage)
        mock_response.content = '{}'
        client._send_message_implementation_specific_logic = MagicMock(return_value=mock_response)
        result = client.send_message_expecting_json_response(message)
        assert isinstance(result, dict)

    def test_send_message_expecting_json_response_invalid_json(self):
        client = MockLlMClient()
        message = 'Give me a JSON response.'
        mock_response = MagicMock(LlmMessage)
        mock_response.content = 'Invalid JSON'
        client._send_message_implementation_specific_logic = MagicMock(return_value=mock_response)
        with pytest.raises(ValueError):
            client.send_message_expecting_json_response(message)

    def test_send_system_message(self):
        client = MockLlMClient()
        response = client.send_message('System setup.')
        assert len(client._memory) == 2
        assert response == 'Response to the message'