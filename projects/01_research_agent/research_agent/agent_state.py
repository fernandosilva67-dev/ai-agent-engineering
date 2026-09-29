from pydantic import BaseModel, Field


class Observation(BaseModel):
    """Result observed by the agent after executing a tool."""

    tool_name: str
    source: str
    content: str


class AgentState(BaseModel):
    """Execution state maintained across agent loop iterations."""

    question: str = Field(min_length=1)
    observations: list[Observation] = Field(default_factory=list)
    step_count: int = Field(default=0, ge=0)
