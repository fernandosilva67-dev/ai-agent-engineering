from typing import TypeVar

from pydantic import BaseModel
from research_agent.decision import ResearchDecision
from research_agent.decision_maker import LLMDecisionMaker

T = TypeVar("T", bound=BaseModel)


class FakeModelClient:
    """Fake model client used for unit tests."""

    def __init__(self, response: BaseModel):
        self.response = response
        self.prompt: str | None = None
        self.output_type: type[BaseModel] | None = None

    def generate(
        self,
        prompt: str,
        output_type: type[T],
    ) -> T:
        self.prompt = prompt
        self.output_type = output_type
        assert isinstance(self.response, output_type)
        return self.response


def test_llm_decision_maker_requests_search():
    client = FakeModelClient(
        ResearchDecision(
            action="search",
            query="AI agent architecture",
        )
    )
    decision_maker = LLMDecisionMaker(client)

    decision = decision_maker.decide("How are AI agents architected?")

    assert decision.action == "search"
    assert decision.query == "AI agent architecture"
    assert "How are AI agents architected?" in client.prompt
    assert "search" in client.prompt.lower()
    assert "final" in client.prompt.lower()
    assert client.output_type is ResearchDecision


def test_llm_decision_maker_returns_final_decision():
    client = FakeModelClient(
        ResearchDecision(
            action="final",
        )
    )
    decision_maker = LLMDecisionMaker(client)

    decision = decision_maker.decide("What is Python?")

    assert decision.action == "final"
    assert decision.query is None
    assert "What is Python?" in client.prompt
    assert "search" in client.prompt.lower()
    assert "final" in client.prompt.lower()
    assert client.output_type is ResearchDecision
