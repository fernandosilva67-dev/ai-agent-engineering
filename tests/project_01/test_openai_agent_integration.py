from typing import Any

from research_agent.agent import ResearchAgent
from research_agent.models import ResearchRequest, ResearchResult
from research_agent.openai_model_session import OpenAIModelSession
from research_agent.tool_executor import ToolExecutor


class FakeResponses:
    """Fake OpenAI Responses API for agent integration testing."""

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
                arguments = '{"query":"Python 3.14 features"}'
                call_id = "call_123"

            class FakeResponse:
                id = "resp_123"
                output = [FakeFunctionCall()]
                output_text = ""

            return FakeResponse()

        class FakeResponse:
            id = "resp_456"
            output = []
            output_text = "Python 3.14 includes several new features."

        return FakeResponse()


class FakeOpenAIClient:
    """Fake OpenAI client isolated from the network."""

    def __init__(self):
        self.responses = FakeResponses()


def test_research_agent_runs_openai_tool_loop_to_final_answer():
    executed_queries: list[str] = []

    def fake_search(query: str) -> ResearchResult:
        executed_queries.append(query)
        return ResearchResult(
            source="fake_search",
            content="Research result about Python 3.14.",
        )

    openai_client = FakeOpenAIClient()

    session = OpenAIModelSession(
        client=openai_client,
        model="test-model",
    )

    agent = ResearchAgent(
        model_session=session,
        tool_executor=ToolExecutor(search_tool=fake_search),
    )

    response = agent.run(
        ResearchRequest(question="What changed in Python 3.14?")
    )

    assert executed_queries == ["Python 3.14 features"]

    assert response.answer == "Python 3.14 includes several new features."
    assert response.sources == ["fake_search"]

    assert openai_client.responses.calls[1]["previous_response_id"] == "resp_123"
    assert openai_client.responses.calls[1]["input"] == [
        {
            "type": "function_call_output",
            "call_id": "call_123",
            "output": "Research result about Python 3.14.",
        }
    ]
