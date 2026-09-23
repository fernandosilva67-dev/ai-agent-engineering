from .decision_maker import DecisionMaker, DeterministicDecisionMaker
from .models import ResearchRequest, ResearchResponse
from .tool_call import SearchToolArguments, ToolCall
from .tool_executor import ToolExecutor
from .tools import search


class ResearchAgent:
    """Basic research agent that orchestrates decisions and tools."""

    def __init__(
        self,
        decision_maker: DecisionMaker | None = None,
        tool_executor: ToolExecutor | None = None,
    ):
        self.decision_maker = decision_maker or DeterministicDecisionMaker()
        self.tool_executor = tool_executor or ToolExecutor(search_tool=search)
        
    def run(self, request: ResearchRequest) -> ResearchResponse:
        """Research the question and return a structured response."""
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
