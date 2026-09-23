from research_agent.agent import ResearchAgent
from research_agent.decision import ResearchDecision
from research_agent.models import ResearchRequest, ResearchResult
from research_agent.tool_call import SearchToolArguments, ToolCall
from research_agent.tool_executor import ToolExecutor


class FinalDecisionMaker:
    """Test double that always returns a final decision."""

    def decide(self, question: str) -> ResearchDecision:
        return ResearchDecision(action="final")

class FakeToolCallingClient:
    """Test double that always requests the search tool."""

    def request_tool_call(self, prompt: str) -> ToolCall | None:
        return ToolCall(
            name="search",
            arguments=SearchToolArguments(query=prompt),
        )

def test_agent_researches_question():
    agent = ResearchAgent()

    response = agent.run(ResearchRequest(question="What is an AI agent?"))

    assert response.answer
    assert "What is an AI agent?" in response.answer
    assert response.sources == ["simulated_search"]


def test_agent_can_return_final_without_searching():
    agent = ResearchAgent(decision_maker=FinalDecisionMaker())

    response = agent.run(ResearchRequest(question="What is an AI agent?"))

    assert response.answer == "What is an AI agent?"
    assert response.sources == []

def test_agent_executes_search_through_tool_executor():
    def fake_search(query: str) -> ResearchResult:
        return ResearchResult(
            source="injected_search",
            content=f"Injected result for: {query}",
        )

    executor = ToolExecutor(search_tool=fake_search)
    agent = ResearchAgent(tool_executor=executor)

    response = agent.run(
        ResearchRequest(question="What is native tool calling?")
    )

    assert response.answer == "Injected result for: What is native tool calling?"
    assert response.sources == ["injected_search"]

def test_agent_executes_model_requested_tool_call():
    def fake_search(query: str) -> ResearchResult:
        return ResearchResult(
            source="native_tool_call",
            content=f"Tool result for: {query}",
        )

    executor = ToolExecutor(search_tool=fake_search)

    agent = ResearchAgent(
        tool_calling_client=FakeToolCallingClient(),
        tool_executor=executor,
    )

    response = agent.run(
        ResearchRequest(question="What is native tool calling?")
    )

    assert response.answer == "Tool result for: What is native tool calling?"
    assert response.sources == ["native_tool_call"]
