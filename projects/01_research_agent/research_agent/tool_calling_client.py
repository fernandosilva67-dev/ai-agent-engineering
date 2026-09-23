from typing import Protocol

from .tool_call import ToolCall


class ToolCallingClient(Protocol):
    """Contract for requesting tool calls from a language model."""

    def request_tool_call(self, prompt: str) -> ToolCall | None:
        """Request a validated tool call from the language model."""
        ...
