from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class OpenAIModelClient:
    """Adapter for structured responses from the OpenAI Responses API."""

    def __init__(self, client: Any, model: str):
        self.client = client
        self.model = model

    def generate(
        self,
        prompt: str,
        output_type: type[T],
    ) -> T:
        """Generate and parse a structured model response."""
        response = self.client.responses.parse(
            model=self.model,
            input=prompt,
            text_format=output_type,
        )

        if response.output_parsed is None:
            raise RuntimeError("OpenAI response did not contain structured output.")

        return response.output_parsed
