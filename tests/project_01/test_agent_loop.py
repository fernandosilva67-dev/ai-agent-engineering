import pytest
from research_agent.agent import ResearchAgent
from research_agent.agent_state import Observation
from research_agent.model_turn import FinalAnswer, ModelTurnResult, ToolRequested
from research_agent.models import ResearchRequest, ResearchResult
from research_agent.tool_call import SearchToolArguments, ToolCall
from research_agent.tool_executor import ToolExecutor


class FakeModelSession:
    """Deterministic model session used to test the agent loop."""

    def __init__(self):
        self.observations: list[Observation] = []
        self.turns: list[ModelTurnResult] = [
            ToolRequested(
                tool_call=ToolCall(
                    name="search",
                    arguments=SearchToolArguments(query="Python 3.14 features"),
                )
            ),
            ToolRequested(
                tool_call=ToolCall(
                    name="search",
                    arguments=SearchToolArguments(query="Python 3.14 performance"),
                )
            ),
            FinalAnswer(
                answer="Python 3.14 includes new features and performance improvements."
            ),
        ]

    def start(self, question: str) -> ModelTurnResult:
        return self.turns.pop(0)

    def continue_with(self, observation: Observation) -> ModelTurnResult:
        self.observations.append(observation)
        return self.turns.pop(0)


def test_agent_loops_until_final_answer():
    executed_queries: list[str] = []

    def fake_search(query: str) -> ResearchResult:
        executed_queries.append(query)
        return ResearchResult(
            source=f"source_{len(executed_queries)}",
            content=f"Result for: {query}",
        )

    session = FakeModelSession()
    executor = ToolExecutor(search_tool=fake_search)

    agent = ResearchAgent(
        model_session=session,
        tool_executor=executor,
    )

    response = agent.run(
        ResearchRequest(question="What changed in Python 3.14?")
    )

    assert executed_queries == [
        "Python 3.14 features",
        "Python 3.14 performance",
    ]

    assert session.observations == [
        Observation(
            tool_name="search",
            source="source_1",
            content="Result for: Python 3.14 features",
        ),
        Observation(
            tool_name="search",
            source="source_2",
            content="Result for: Python 3.14 performance",
        ),
    ]

    assert response.answer == (
        "Python 3.14 includes new features and performance improvements."
    )
    assert response.sources == ["source_1", "source_2"]


class EndlessToolModelSession:
    """Model session that never produces a final answer."""

    def start(self, question: str) -> ModelTurnResult:
        return self._tool_request()

    def continue_with(self, observation: Observation) -> ModelTurnResult:
        return self._tool_request()

    def _tool_request(self) -> ToolRequested:
        return ToolRequested(
            tool_call=ToolCall(
                name="search",
                arguments=SearchToolArguments(query="repeat forever"),
            )
        )


def test_agent_stops_when_max_steps_is_reached():
    executed_queries: list[str] = []

    def fake_search(query: str) -> ResearchResult:
        executed_queries.append(query)
        return ResearchResult(
            source="fake_search",
            content=f"Result for: {query}",
        )

    agent = ResearchAgent(
        model_session=EndlessToolModelSession(),
        tool_executor=ToolExecutor(search_tool=fake_search),
        max_steps=2,
    )

    with pytest.raises(RuntimeError, match="maximum number of steps"):
        agent.run(ResearchRequest(question="Never-ending research"))

    assert executed_queries == [
        "repeat forever",
        "repeat forever",
    ]


def test_agent_rejects_non_positive_max_steps():
    with pytest.raises(ValueError, match="max_steps must be at least 1"):
        ResearchAgent(max_steps=0)

    with pytest.raises(ValueError, match="max_steps must be at least 1"):
        ResearchAgent(max_steps=-1)
