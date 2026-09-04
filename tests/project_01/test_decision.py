import pytest
from pydantic import ValidationError

from research_agent.decision import ResearchDecision


def test_search_decision_requires_query():
    decision = ResearchDecision(
        action="search",
        query="What is an AI agent?",
    )

    assert decision.action == "search"
    assert decision.query == "What is an AI agent?"


def test_final_decision_does_not_require_query():
    decision = ResearchDecision(action="final")

    assert decision.action == "final"
    assert decision.query is None


def test_invalid_action_is_rejected():
    with pytest.raises(ValidationError):
        ResearchDecision(action="invalid")
