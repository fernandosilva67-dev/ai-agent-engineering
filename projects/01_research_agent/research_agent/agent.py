from .decision_maker import DecisionMaker, DeterministicDecisionMaker
from .models import ResearchRequest, ResearchResponse
from .tools import search


class ResearchAgent:
    """Basic research agent that orchestrates decisions and tools."""

    def __init__(self, decision_maker: DecisionMaker | None = None):
        self.decision_maker = decision_maker or DeterministicDecisionMaker()

    def run(self, request: ResearchRequest) -> ResearchResponse:
        """Research the question and return a structured response."""
        decision = self.decision_maker.decide(request.question)

        if decision.action == "search":
            result = search(decision.query or request.question)

            return ResearchResponse(
                answer=result.content,
                sources=[result.source],
            )

        return ResearchResponse(
            answer=request.question,
            sources=[],
        )
