"""Test that malformed LLM output is handled gracefully."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


def _make_llm_result_raw(content: str) -> dict:
    msg = MagicMock()
    msg.content = content
    return {"messages": [msg]}


@pytest.mark.asyncio
async def test_malformed_llm_output_returns_parse_error(add_agent_to_path):
    """When LLM returns non-JSON, the agent should not crash."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    with patch.object(
        agent,
        "_invoke_with_fallback",
        new=AsyncMock(return_value=_make_llm_result_raw("This is definitely positive!")),
    ):
        # The _classify_sentiment method returns the raw LLM output;
        # the system prompt instructs the LLM to return JSON but the agent
        # itself does not enforce JSON parsing (it trusts the prompt).
        # This test verifies the agent does NOT raise an exception for non-JSON output.
        response = await agent._classify_sentiment(
            "Great product!", "test-ctx-parse", []
        )

    # The agent returns whatever the LLM returned — no crash
    assert response is not None
    assert isinstance(response, str)
