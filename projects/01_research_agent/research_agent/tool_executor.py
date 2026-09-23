from collections.abc import Callable

from .models import ResearchResult
from .tool_call import ToolCall


class ToolExecutor:
    """Execute validated tool calls using injected tool implementations."""

    def __init__(
        self,
        search_tool: Callable[[str], ResearchResult],
    ):
        self.search_tool = search_tool

    def execute(self, call: ToolCall) -> ResearchResult:
        """Execute a validated tool call."""
        return self.search_tool(call.arguments.query)
