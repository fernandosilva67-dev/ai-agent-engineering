from research_agent.tools import search


def test_search_returns_research_result():
    result = search("What is an AI agent?")

    assert result.source == "simulated_search"
    assert "What is an AI agent?" in result.content
