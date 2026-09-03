from agents.core.types import AgentRequest, AgentResponse


def test_agent_request_accepts_valid_prompt():
    request = AgentRequest(prompt="What is an AI agent?")

    assert request.prompt == "What is an AI agent?"


def test_agent_response_contains_answer():
    response = AgentResponse(answer="An AI agent can reason and use tools.")

    assert response.answer.startswith("An AI agent")
