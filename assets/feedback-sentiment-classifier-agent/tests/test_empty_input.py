"""Test that empty or whitespace-only input returns a structured error."""
import json
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


@pytest.mark.asyncio
async def test_empty_string_returns_error(add_agent_to_path):
    """Empty string input returns the empty_input structured error."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    response = await agent._classify_sentiment("", "test-ctx-empty", [])
    data = json.loads(response)
    assert data["error"] == "empty_input"
    assert "message" in data


@pytest.mark.asyncio
async def test_whitespace_only_returns_error(add_agent_to_path):
    """Whitespace-only input returns the empty_input structured error."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    response = await agent._classify_sentiment("   \n  ", "test-ctx-ws", [])
    data = json.loads(response)
    assert data["error"] == "empty_input"
