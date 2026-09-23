from typing import Literal

from pydantic import BaseModel, Field


class SearchToolArguments(BaseModel):
    """Validated arguments for the search tool."""

    query: str = Field(min_length=1)


class ToolCall(BaseModel):
    """Structured request to invoke a tool."""

    name: Literal["search"]
    arguments: SearchToolArguments
