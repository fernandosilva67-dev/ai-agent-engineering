from research_agent.models import ResearchResult
from research_agent.tool_call import SearchToolArguments, ToolCall
from research_agent.tool_executor import ToolExecutor


def fake_search(query: str) -> ResearchResult:
    return ResearchResult(
        source="fake_search",
        content=f"Result for: {query}",
    )


def test_executor_executes_search_tool():
    executor = ToolExecutor(search_tool=fake_search)

    call = ToolCall(
        name="search",
        arguments=SearchToolArguments(query="Python 3.14 new features"),
    )

    result = executor.execute(call)

    assert result.source == "fake_search"
    assert result.content == "Result for: Python 3.14 new features"
