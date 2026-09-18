"""Test that neutral/factual feedback is classified correctly."""
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
async def test_neutral_feedback_classification(add_agent_to_path):
    """Neutral feedback returns sentiment=neutral."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    with patch.object(
        agent,
        "_invoke_with_fallback",
        new=AsyncMock(return_value=_make_llm_result("neutral", 0.80)),
    ):
        response = await agent._classify_sentiment(
            "The package arrived on Tuesday.", "test-ctx-neu", []
        )

    data = json.loads(response)
    assert data["sentiment"] == "neutral"
    assert data["confidence"] == 0.80
    assert "error" not in data
