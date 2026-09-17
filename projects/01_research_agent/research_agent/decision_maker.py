from typing import TYPE_CHECKING, Protocol

from .decision import ResearchDecision

if TYPE_CHECKING:
    from .model_client import ModelClient


class DecisionMaker(Protocol):
    """Contract for components that decide the agent's next action."""

    def decide(self, question: str) -> ResearchDecision:
        """Return the next action for a research question."""
        ...


class DeterministicDecisionMaker:
    """Simple decision maker used before introducing an LLM."""

    def decide(self, question: str) -> ResearchDecision:
        """Always request a search."""
        return ResearchDecision(
            action="search",
            query=question,
        )


class LLMDecisionMaker:
    """Decision maker that delegates decisions to a language model."""

    def __init__(self, client: ModelClient):
        self.client = client

    def decide(self, question: str) -> ResearchDecision:
        """Use a language model to decide the next research action."""
        prompt = f"""
        Decide the next action for the research agent.

        Choose:
        - "search" when external research is needed to answer the question.
        - "final" when no external research is needed.

        If the action is "search", provide a concise search query.
        If the action is "final", the query must be null.

        User question:
        {question}
        """.strip()

        return self.client.generate(
            prompt=prompt,
            output_type=ResearchDecision,
        )
