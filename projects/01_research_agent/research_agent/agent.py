from .agent_state import AgentState, Observation
from .decision_maker import DecisionMaker, DeterministicDecisionMaker
from .model_session import ModelSession
from .model_turn import FinalAnswer, ToolRequested
from .models import ResearchRequest, ResearchResponse
from .tool_call import SearchToolArguments, ToolCall
from .tool_calling_client import ToolCallingClient
from .tool_executor import ToolExecutor
from .tools import search


class ResearchAgent:
    """Basic research agent that orchestrates decisions and tools."""

    def __init__(
        self,
        decision_maker: DecisionMaker | None = None,
        tool_executor: ToolExecutor | None = None,
        tool_calling_client: ToolCallingClient | None = None,
        model_session: ModelSession | None = None,
        max_steps: int = 5,
    ):
        self.decision_maker = decision_maker or DeterministicDecisionMaker()
        self.tool_executor = tool_executor or ToolExecutor(search_tool=search)
        self.tool_calling_client = tool_calling_client
        self.model_session = model_session

        if max_steps < 1:
            raise ValueError("max_steps must be at least 1")

        self.max_steps = max_steps

    def run(self, request: ResearchRequest) -> ResearchResponse:
        """Research the question and return a structured response."""
        if self.model_session is not None:
            state = AgentState(question=request.question)
            turn = self.model_session.start(state.question)

            while True:
                if isinstance(turn, FinalAnswer):
                    return ResearchResponse(
                        answer=turn.answer,
                        sources=[
                            observation.source
                            for observation in state.observations
                        ],
                    )

                if isinstance(turn, ToolRequested):
                    if state.step_count >= self.max_steps:
                        raise RuntimeError(
                            "Agent reached the maximum number of steps."
                        )

                    result = self.tool_executor.execute(turn.tool_call)

                    observation = Observation(
                        tool_name=turn.tool_call.name,
                        source=result.source,
                        content=result.content,
                    )

                    state.observations.append(observation)
                    state.step_count += 1

                    turn = self.model_session.continue_with(observation)

        if self.tool_calling_client is not None:
            call = self.tool_calling_client.request_tool_call(request.question)

            if call is not None:
                result = self.tool_executor.execute(call)

                return ResearchResponse(
                    answer=result.content,
                    sources=[result.source],
                )

        decision = self.decision_maker.decide(request.question)

        if decision.action == "search":
            call = ToolCall(
                name="search",
                arguments=SearchToolArguments(query=decision.query),
            )
            result = self.tool_executor.execute(call)

            return ResearchResponse(
                answer=result.content,
                sources=[result.source],
            )

        return ResearchResponse(
            answer=request.question,
            sources=[],
        )
