from typing import Literal

from pydantic import BaseModel


class ResearchDecision(BaseModel):
    """Decision made by the research agent."""

    action: Literal["search", "final"]
    query: str | None = None
