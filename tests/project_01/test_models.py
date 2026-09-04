from research_agent.models import (
    ResearchRequest,
    ResearchResponse,
    ResearchResult,
)


def test_research_request_accepts_question():
    request = ResearchRequest(question="What is an AI agent?")

    assert request.question == "What is an AI agent?"


def test_research_result_contains_source_and_content():
    result = ResearchResult(
        source="test_source",
        content="Test research content.",
    )

    assert result.source == "test_source"
    assert result.content == "Test research content."


def test_research_response_contains_answer_and_sources():
    response = ResearchResponse(
        answer="An AI agent can reason and use tools.",
        sources=["test_source"],
    )

    assert response.answer.startswith("An AI agent")
    assert response.sources == ["test_source"]
