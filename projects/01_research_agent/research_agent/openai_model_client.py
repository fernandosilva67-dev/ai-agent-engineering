import json
from typing import Any, TypeVar

from pydantic import BaseModel

from .tool_call import SearchToolArguments, ToolCall

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

    def request_tool_call(self, prompt: str) -> ToolCall | None:
        """Request and parse a tool call from the language model."""
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            tools=[
                {
                    "type": "function",
                    "name": "search",
                    "description": "Search for information relevant to the user's question.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                }
            ],
        )

        for item in response.output:
            if item.type == "function_call" and item.name == "search":
                arguments = SearchToolArguments.model_validate(
                    json.loads(item.arguments)
                )
                return ToolCall(
                    name="search",
                    arguments=arguments,
                )

        return None
