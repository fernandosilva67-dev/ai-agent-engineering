import json
from typing import Any

from .agent_state import Observation
from .model_turn import FinalAnswer, ModelTurnResult, ToolRequested
from .tool_call import SearchToolArguments, ToolCall


class OpenAIModelSession:
    """Stateful adapter for iterative OpenAI Responses API interactions."""

    def __init__(self, client: Any, model: str):
        self.client = client
        self.model = model
        self._previous_response_id: str | None = None
        self._pending_call_id: str | None = None

    def start(self, question: str) -> ModelTurnResult:
        """Start a model session for a research question."""
        response = self.client.responses.create(
            model=self.model,
            input=question,
            tools=self._tools(),
        )

        return self._parse_response(response)

    def continue_with(self, observation: Observation) -> ModelTurnResult:
        """Continue the model session with the result of a tool call."""
        if self._previous_response_id is None:
            raise RuntimeError("Model session has not been started.")

        if self._pending_call_id is None:
            raise RuntimeError("Model session has no pending tool call.")

        response = self.client.responses.create(
            model=self.model,
            previous_response_id=self._previous_response_id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": self._pending_call_id,
                    "output": observation.content,
                }
            ],
            tools=self._tools(),
        )

        return self._parse_response(response)

    def _parse_response(self, response: Any) -> ModelTurnResult:
        """Convert an OpenAI response into a provider-independent model turn."""
        self._previous_response_id = response.id
        self._pending_call_id = None

        for item in response.output:
            if item.type == "function_call" and item.name == "search":
                self._pending_call_id = item.call_id

                arguments = SearchToolArguments.model_validate(
                    json.loads(item.arguments)
                )

                return ToolRequested(
                    tool_call=ToolCall(
                        name="search",
                        arguments=arguments,
                    )
                )

        if response.output_text:
            return FinalAnswer(answer=response.output_text)

        raise RuntimeError(
            "OpenAI response contained neither a tool call nor a final answer."
        )

    @staticmethod
    def _tools() -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "name": "search",
                "description": (
                    "Search for information relevant to the user's question."
                ),
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
        ]
