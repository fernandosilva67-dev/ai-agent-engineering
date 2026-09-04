from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Input received by the research agent."""

    question: str = Field(min_length=1)


class ResearchResult(BaseModel):
    """Result returned by a research tool."""

    source: str
    content: str


class ResearchResponse(BaseModel):
    """Final structured response produced by the research agent."""

    answer: str
    sources: list[str] = Field(default_factory=list)
