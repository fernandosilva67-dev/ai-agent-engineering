from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Input received by an agent."""

    prompt: str = Field(min_length=1)


class AgentResponse(BaseModel):
    """Structured response returned by an agent."""

    answer: str
