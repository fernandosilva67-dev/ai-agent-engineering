from .models import ResearchResult


def search(query: str) -> ResearchResult:
    """Simulate a research search tool."""

    return ResearchResult(
        source="simulated_search",
        content=f"Simulated research result for: {query}",
    )
