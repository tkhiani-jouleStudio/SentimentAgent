"""Integration test: end-to-end agent flow via invoke()."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


def _make_llm_result(sentiment: str, confidence: float) -> dict:
    payload = json.dumps({"sentiment": sentiment, "confidence": confidence})
    msg = MagicMock()
    msg.content = payload
    return {"messages": [msg]}


@pytest.mark.asyncio
async def test_end_to_end_positive_invoke(add_agent_to_path):
    """Full invoke() call for positive feedback returns completed status with JSON content."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    with patch.object(
        agent,
        "_invoke_with_fallback",
        new=AsyncMock(return_value=_make_llm_result("positive", 0.97)),
    ):
        result = await agent.invoke(
            "This is the best service I have ever received!", "test-ctx-e2e", tools=[]
        )

    assert result.status == "completed"
    data = json.loads(result.message)
    assert data["sentiment"] == "positive"
    assert data["confidence"] == 0.97


@pytest.mark.asyncio
async def test_end_to_end_empty_input(add_agent_to_path):
    """Full invoke() for empty input returns error JSON without calling LLM."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    llm_mock = AsyncMock()
    with patch.object(agent, "_invoke_with_fallback", new=llm_mock):
        result = await agent.invoke("", "test-ctx-e2e-empty", tools=[])

    # LLM must NOT have been called for empty input
    llm_mock.assert_not_called()
    assert result.status == "completed"
    data = json.loads(result.message)
    assert data["error"] == "empty_input"
