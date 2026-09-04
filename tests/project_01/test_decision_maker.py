from research_agent.decision_maker import DeterministicDecisionMaker


def test_decision_maker_requests_search():
    decision_maker = DeterministicDecisionMaker()

    decision = decision_maker.decide("What is an AI agent?")

    assert decision.action == "search"
    assert decision.query == "What is an AI agent?"
