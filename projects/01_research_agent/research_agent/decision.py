from typing import Literal

from pydantic import BaseModel, model_validator


class ResearchDecision(BaseModel):
    """Decision made by the research agent."""

    action: Literal["search", "final"]
    query: str | None = None

    @model_validator(mode="after")
    def validate_query(self) -> "ResearchDecision":
        """Ensure search decisions contain a query."""
        if self.action == "search" and not self.query:
            raise ValueError("Search decisions require a query.")

        if self.action == "final" and self.query is not None:
            raise ValueError("Final decisions must not contain a query.")

        return self
