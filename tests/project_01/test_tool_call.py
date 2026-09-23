import pytest
from pydantic import ValidationError
from research_agent.tool_call import SearchToolArguments, ToolCall


def test_search_tool_call_contains_validated_arguments():
    call = ToolCall(
        name="search",
        arguments=SearchToolArguments(query="Python 3.14 new features"),
    )

    assert call.name == "search"
    assert call.arguments.query == "Python 3.14 new features"

def test_search_tool_call_rejects_empty_query():
    with pytest.raises(ValidationError):
        ToolCall(
            name="search",
            arguments=SearchToolArguments(query=""),
        )
