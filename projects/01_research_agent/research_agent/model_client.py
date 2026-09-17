from typing import Protocol, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class ModelClient(Protocol):
    """Contract for structured interactions with a language model."""

    def generate(
        self,
        prompt: str,
        output_type: type[T],
    ) -> T:
        """Generate a structured response matching the requested output type."""
        ...
