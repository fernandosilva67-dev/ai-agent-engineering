from typing import Any

import pytest
from research_agent.decision import ResearchDecision
from research_agent.openai_model_client import OpenAIModelClient
from research_agent.tool_call import SearchToolArguments, ToolCall


class FakeResponses:
    """Fake Responses API used for unit tests."""

    def __init__(self, parsed_output: ResearchDecision | None):
        self.parsed_output = parsed_output
        self.calls: list[dict[str, Any]] = []

    def parse(
        self,
        *,
        model: str,
        input: str,
        text_format: type[ResearchDecision],
    ):
        self.calls.append(
            {
                "model": model,
                "input": input,
                "text_format": text_format,
            }
        )

        class FakeResponse:
            output_parsed = self.parsed_output

        return FakeResponse()

    def create(
        self,
        *,
        model: str,
        input: str,
        tools: list[dict[str, Any]],
    ):
        self.calls.append(
            {
                "model": model,
                "input": input,
                "tools": tools,
            }
        )

        class FakeFunctionCall:
            type = "function_call"
            name = "search"
            arguments = '{"query":"Python 3.14 new features"}'
            call_id = "call_123"

        class FakeResponse:
            output = [FakeFunctionCall()]

        return FakeResponse()

class FakeOpenAIClient:
    """Fake OpenAI client used to isolate the adapter from the network."""

    def __init__(self, parsed_output: ResearchDecision | None):
        self.responses = FakeResponses(parsed_output)


def test_openai_model_client_generates_structured_output():
    expected = ResearchDecision(
        action="search",
        query="AI agent architecture",
    )
    openai_client = FakeOpenAIClient(expected)
    client = OpenAIModelClient(
        client=openai_client,
        model="test-model",
    )

    result = client.generate(
        prompt="Decide the next action.",
        output_type=ResearchDecision,
    )

    assert result == expected
    assert openai_client.responses.calls == [
        {
            "model": "test-model",
            "input": "Decide the next action.",
            "text_format": ResearchDecision,
        }
    ]


def test_openai_model_client_rejects_missing_structured_output():
    openai_client = FakeOpenAIClient(None)
    client = OpenAIModelClient(
        client=openai_client,
        model="test-model",
    )

    with pytest.raises(RuntimeError, match="structured output"):
        client.generate(
            prompt="Decide the next action.",
            output_type=ResearchDecision,
        )


def test_openai_model_client_requests_search_tool():
    openai_client = FakeOpenAIClient(None)
    client = OpenAIModelClient(
        client=openai_client,
        model="test-model",
    )

    result = client.request_tool_call(
        prompt="What are the new features in Python 3.14?",
    )

    assert openai_client.responses.calls == [
        {
            "model": "test-model",
            "input": "What are the new features in Python 3.14?",
            "tools": [
                {
                    "type": "function",
                    "name": "search",
                    "description": (
                        "Search for information relevant to the user's question."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            ],
        }
    ]
    assert result == ToolCall(
        name="search",
        arguments=SearchToolArguments(
            query="Python 3.14 new features",
        ),
    )
