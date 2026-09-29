import pytest
from pydantic import ValidationError
from research_agent.agent_state import AgentState, Observation


def test_agent_state_starts_without_observations():
    state = AgentState(question="What changed in Python 3.14?")

    assert state.question == "What changed in Python 3.14?"
    assert state.observations == []
    assert state.step_count == 0


def test_agent_state_accepts_observations():
    observation = Observation(
        tool_name="search",
        source="fake_search",
        content="Python 3.14 introduces new language features.",
    )

    state = AgentState(
        question="What changed in Python 3.14?",
        observations=[observation],
        step_count=1,
    )

    assert state.observations == [observation]
    assert state.step_count == 1


def test_agent_state_rejects_empty_question():
    with pytest.raises(ValidationError):
        AgentState(question="")


def test_agent_state_rejects_negative_step_count():
    with pytest.raises(ValidationError):
        AgentState(
            question="What changed in Python 3.14?",
            step_count=-1,
        )
