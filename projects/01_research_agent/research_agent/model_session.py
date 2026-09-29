from typing import Protocol

from .agent_state import Observation
from .model_turn import ModelTurnResult


class ModelSession(Protocol):
    """Contract for an iterative model interaction within one agent run."""

    def start(self, question: str) -> ModelTurnResult:
        """Start the model interaction for a question."""
        ...

    def continue_with(self, observation: Observation) -> ModelTurnResult:
        """Continue the interaction after a tool observation."""
        ...
