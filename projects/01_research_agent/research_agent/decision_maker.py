from typing import Protocol

from .decision import ResearchDecision


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
