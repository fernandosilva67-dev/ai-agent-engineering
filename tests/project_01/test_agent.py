from research_agent.agent import ResearchAgent
from research_agent.models import ResearchRequest


def test_agent_researches_question():
    agent = ResearchAgent()

    response = agent.run(
        ResearchRequest(question="What is an AI agent?")
    )

    assert response.answer
    assert "What is an AI agent?" in response.answer
    assert response.sources == ["simulated_search"]
