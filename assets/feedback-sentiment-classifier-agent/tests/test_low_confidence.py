"""Test that low-confidence responses include the low_confidence flag."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def add_app_to_path(add_agent_to_path):
    pass


def _make_llm_result(sentiment: str, confidence: float, extra: dict | None = None) -> dict:
    payload = {"sentiment": sentiment, "confidence": confidence}
    if extra:
        payload.update(extra)
    msg = MagicMock()
    msg.content = json.dumps(payload)
    return {"messages": [msg]}


@pytest.mark.asyncio
async def test_low_confidence_flag_present(add_agent_to_path):
    """When confidence < 0.7, the response should include low_confidence=true."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    # LLM returns confidence 0.65 with low_confidence flag already set by model
    with patch.object(
        agent,
        "_invoke_with_fallback",
        new=AsyncMock(return_value=_make_llm_result("neutral", 0.65, {"low_confidence": True})),
    ):
        response = await agent._classify_sentiment(
            "It was okay I guess.", "test-ctx-lc", []
        )

    data = json.loads(response)
    assert data["sentiment"] == "neutral"
    assert data["confidence"] == 0.65
    assert data.get("low_confidence") is True


@pytest.mark.asyncio
async def test_high_confidence_no_flag(add_agent_to_path):
    """When confidence >= 0.7, the low_confidence flag should not be present."""
    with patch("agent.ChatLiteLLM"), \
         patch("agent.create_checkpointer", return_value=MagicMock()), \
         patch("agent.SummarizationMiddleware"), \
         patch("agent.CircuitBreaker"):
        from agent import SampleAgent
        agent = SampleAgent()

    with patch.object(
        agent,
        "_invoke_with_fallback",
        new=AsyncMock(return_value=_make_llm_result("positive", 0.92)),
    ):
        response = await agent._classify_sentiment(
            "Absolutely love this!", "test-ctx-hc", []
        )

    data = json.loads(response)
    assert data.get("low_confidence") is not True
