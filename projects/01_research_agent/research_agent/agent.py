from .models import ResearchRequest, ResearchResponse
from .tools import search


class ResearchAgent:
    """Basic research agent that orchestrates a search tool."""

    def run(self, request: ResearchRequest) -> ResearchResponse:
        """Research the question and return a structured response."""

        result = search(request.question)

        return ResearchResponse(
            answer=result.content,
            sources=[result.source],
        )
