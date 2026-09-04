from research_agent.agent import ResearchAgent
from research_agent.decision import ResearchDecision
from research_agent.models import ResearchRequest


class FinalDecisionMaker:
    """Test double that always returns a final decision."""

    def decide(self, question: str) -> ResearchDecision:
        return ResearchDecision(action="final")


def test_agent_researches_question():
    agent = ResearchAgent()

    response = agent.run(
        ResearchRequest(question="What is an AI agent?")
    )

    assert response.answer
    assert "What is an AI agent?" in response.answer
    assert response.sources == ["simulated_search"]


def test_agent_can_return_final_without_searching():
    agent = ResearchAgent(
        decision_maker=FinalDecisionMaker()
    )

    response = agent.run(
        ResearchRequest(question="What is an AI agent?")
    )

    assert response.answer == "What is an AI agent?"
    assert response.sources == []
