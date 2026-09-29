import pytest
from pydantic import ValidationError
from research_agent.model_turn import FinalAnswer, ToolRequested
from research_agent.tool_call import SearchToolArguments, ToolCall


def test_tool_requested_contains_tool_call():
    call = ToolCall(
        name="search",
        arguments=SearchToolArguments(query="Python 3.14 new features"),
    )

    turn = ToolRequested(tool_call=call)

    assert turn.tool_call == call


def test_final_answer_contains_answer():
    turn = FinalAnswer(answer="Python 3.14 introduces several new features.")

    assert turn.answer == "Python 3.14 introduces several new features."


def test_final_answer_rejects_empty_answer():
    with pytest.raises(ValidationError):
        FinalAnswer(answer="")
