from pydantic import BaseModel, Field

from .tool_call import ToolCall


class ToolRequested(BaseModel):
    """Model turn requesting execution of a tool."""

    tool_call: ToolCall


class FinalAnswer(BaseModel):
    """Model turn containing the final answer."""

    answer: str = Field(min_length=1)


ModelTurnResult = ToolRequested | FinalAnswer
