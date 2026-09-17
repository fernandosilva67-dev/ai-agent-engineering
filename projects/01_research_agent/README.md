# Research Agent

Project 01 of the **AI Agent Engineering** learning path.

The project incrementally builds a research agent while keeping decision logic,
model integration, tool execution, and orchestration separated.

## Current Version

**v0.3 — LLM Decision Maker**

The agent can use a language model to decide whether a question requires
external research.

The decision is represented by a validated Pydantic model:

```python
ResearchDecision(
    action="search" | "final",
    query=str | None,
)
```

The domain invariants are:

- `search` requires a non-empty `query`.
- `final` requires `query=None`.

## Evolution

### v0.1 — Basic Research Agent

Introduced the first orchestration flow:

```text
ResearchRequest
      ↓
ResearchAgent
      ↓
search()
      ↓
ResearchResponse
```

The agent always executed the simulated search tool.

### v0.2 — Decision Layer

Separated decision-making from orchestration through the `DecisionMaker`
protocol.

```text
ResearchAgent
      ↓
DecisionMaker
      ↓
ResearchDecision
```

`DeterministicDecisionMaker` initially always selected `search`.

This version also introduced explicit domain invariants for
`ResearchDecision`.

### v0.3 — LLM Decision Maker

Introduces model-driven decisions while preserving the existing domain
boundaries.

```text
ResearchAgent
      │
      ▼
DecisionMaker
      ▲
      ├── DeterministicDecisionMaker
      │
      └── LLMDecisionMaker
               │
               ▼
          ModelClient
               ▲
               │
        OpenAIModelClient
               │
               ▼
       OpenAI Responses API
```

`LLMDecisionMaker` owns the research decision prompt.

`ModelClient` defines a provider-independent contract for structured model
responses.

`OpenAIModelClient` adapts the OpenAI Responses API to that contract.

The OpenAI integration uses structured outputs parsed directly into Pydantic
models.

## Decision Examples

A question requiring current external information can produce:

```text
Question:
What is the current price of Bitcoin?

Decision:
action='search'
query='current Bitcoin price USD live'
```

A question that does not require external research can produce:

```text
Question:
What is 2 + 2?

Decision:
action='final'
query=None
```

The exact search query is model-generated and may vary.

## Project Structure

```text
projects/01_research_agent/
├── README.md
└── research_agent/
    ├── __init__.py
    ├── agent.py
    ├── decision.py
    ├── decision_maker.py
    ├── model_client.py
    ├── models.py
    ├── openai_model_client.py
    └── tools.py

tests/project_01/
├── test_agent.py
├── test_decision.py
├── test_decision_maker.py
├── test_llm_decision_maker.py
├── test_models.py
├── test_openai_model_client.py
└── test_tools.py
```

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure:

```dotenv
OPENAI_API_KEY=<your-api-key>
OPENAI_MODEL=<model-name>
```

Never commit `.env` or API credentials.

## Tests

Unit tests use fake model clients and fake OpenAI responses.

They do **not** require network access or an OpenAI API key.

Run the complete test suite:

```bash
pytest -q
```

Quality checks:

```bash
ruff check projects/01_research_agent/research_agent tests/project_01
ruff format --check projects/01_research_agent/research_agent tests/project_01
```

At the completion of v0.3:

```text
18 tests passed
```

## Current Limitations

v0.3 deliberately focuses only on model-driven decision-making.

The project does not yet provide:

- real external search;
- model-native tool calling;
- an autonomous agent loop;
- persistent agent state;
- planning;
- memory;
- production observability.

The current `search()` implementation remains simulated.

The `final` path also remains a placeholder and does not yet generate a
complete LLM answer.

These limitations are intentional so that each agent capability is introduced
and tested independently.

## Next Step

**v0.4 — Tool Calling**

The next version will introduce real tool interaction while preserving the
decision and model boundaries established in v0.2 and v0.3.
