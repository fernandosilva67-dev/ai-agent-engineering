from typing import Any

import pytest
from research_agent.agent_state import Observation
from research_agent.model_turn import FinalAnswer, ToolRequested
from research_agent.openai_model_session import OpenAIModelSession
from research_agent.tool_call import SearchToolArguments, ToolCall


class FakeResponses:
    """Fake Responses API for OpenAI model session tests."""

    def __init__(self):
        self.calls: list[dict[str, Any]] = []

    def create(
        self,
        *,
        model: str,
        input: Any,
        tools: list[dict[str, Any]],
        previous_response_id: str | None = None,
    ):
        self.calls.append(
            {
                "model": model,
                "input": input,
                "tools": tools,
                "previous_response_id": previous_response_id,
            }
        )

        if len(self.calls) == 1:
            class FakeFunctionCall:
                type = "function_call"
                name = "search"
                arguments = '{"query":"Python 3.14 new features"}'
                call_id = "call_123"

            class FakeResponse:
                id = "resp_123"
                output = [FakeFunctionCall()]
                output_text = ""

            return FakeResponse()

        class FakeResponse:
            id = "resp_456"
            output = []
            output_text = "Python 3.14 includes new features."

        return FakeResponse()


class FakeOpenAIClient:
    """Fake OpenAI client isolated from the network."""

    def __init__(self):
        self.responses = FakeResponses()


def test_openai_model_session_starts_with_tool_request():
    openai_client = FakeOpenAIClient()
    session = OpenAIModelSession(
        client=openai_client,
        model="test-model",
    )

    turn = session.start("What changed in Python 3.14?")

    assert turn == ToolRequested(
        tool_call=ToolCall(
            name="search",
            arguments=SearchToolArguments(
                query="Python 3.14 new features",
            ),
        )
    )

    assert openai_client.responses.calls[0]["model"] == "test-model"
    assert openai_client.responses.calls[0]["input"] == (
        "What changed in Python 3.14?"
    )
    assert openai_client.responses.calls[0]["previous_response_id"] is None


def test_openai_model_session_continues_with_tool_output():
    openai_client = FakeOpenAIClient()
    session = OpenAIModelSession(
        client=openai_client,
        model="test-model",
    )

    session.start("What changed in Python 3.14?")

    turn = session.continue_with(
        Observation(
            tool_name="search",
            source="fake_search",
            content="Python 3.14 adds several new features.",
        )
    )

    assert turn == FinalAnswer(
        answer="Python 3.14 includes new features."
    )

    assert openai_client.responses.calls[1] == {
        "model": "test-model",
        "input": [
            {
                "type": "function_call_output",
                "call_id": "call_123",
                "output": "Python 3.14 adds several new features.",
            }
        ],
        "tools": openai_client.responses.calls[0]["tools"],
        "previous_response_id": "resp_123",
    }


def test_openai_model_session_rejects_continuation_before_start():
    openai_client = FakeOpenAIClient()
    session = OpenAIModelSession(
        client=openai_client,
        model="test-model",
    )

    with pytest.raises(RuntimeError, match="has not been started"):
        session.continue_with(
            Observation(
                tool_name="search",
                source="fake_search",
                content="Tool result.",
            )
        )


def test_openai_model_session_rejects_continuation_without_pending_tool_call():
    openai_client = FakeOpenAIClient()
    session = OpenAIModelSession(
        client=openai_client,
        model="test-model",
    )

    session.start("What changed in Python 3.14?")

    session.continue_with(
        Observation(
            tool_name="search",
            source="fake_search",
            content="Python 3.14 adds several new features.",
        )
    )

    with pytest.raises(RuntimeError, match="no pending tool call"):
        session.continue_with(
            Observation(
                tool_name="search",
                source="fake_search",
                content="Unexpected additional result.",
            )
        )
