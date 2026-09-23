# AI Agent Engineering — Architecture

This document describes the architecture of the AI Agent Engineering repository and the progressive evolution of Project 01 — Research Agent.

The architecture follows an incremental engineering principle:

**Introduce abstractions only when they solve a concrete architectural problem.**

The objective is to understand the mechanisms behind AI agent frameworks before delegating those mechanisms to higher-level orchestration libraries.

---

# 1. Project 01 — Research Agent

The Research Agent is developed incrementally.

Each version introduces one major architectural capability while preserving the concepts, tests and boundaries established in previous versions.

Current evolution:

| Version | Module | Architectural capability |
|---|---|---|
| v0.1 | M01 | Basic Agent |
| v0.2 | M02 | Decision Layer |
| v0.3 | M03 | LLM Decision Maker |
| v0.4 | M04 | Native Tool Calling |
| v0.5 | M05 | Agent Loop & State — planned |

The current implementation is **Research Agent v0.4**.

---

# 2. Current Package Structure

The Research Agent package is located at:

`projects/01_research_agent/research_agent/`

Current modules:

    research_agent/
    ├── __init__.py
    ├── agent.py
    ├── decision.py
    ├── decision_maker.py
    ├── model_client.py
    ├── models.py
    ├── openai_model_client.py
    ├── tool_call.py
    ├── tool_calling_client.py
    ├── tool_executor.py
    └── tools.py

Each module has a deliberately limited responsibility.

---

# 3. Architectural Overview

The current architecture separates orchestration, decisions, model integration, tool requests and tool execution.

Conceptually:

    ResearchRequest
          │
          ▼
    ResearchAgent
          │
          ├──────────── Decision Layer
          │                 │
          │                 ├── DecisionMaker
          │                 ├── DeterministicDecisionMaker
          │                 └── LLMDecisionMaker
          │
          ├──────────── Model Integration
          │                 │
          │                 ├── ModelClient
          │                 ├── ToolCallingClient
          │                 └── OpenAIModelClient
          │
          └──────────── Tool Layer
                            │
                            ├── ToolCall
                            ├── SearchToolArguments
                            ├── ToolExecutor
                            └── search()
                                  │
                                  ▼
                           ResearchResult
                                  │
                                  ▼
                          ResearchResponse

The `ResearchAgent` acts as the orchestration boundary.

It coordinates components but does not contain provider-specific API logic or the implementation details of external tools.

---

# 4. Core Models

The core request and response models are defined in `models.py`.

## ResearchRequest

Represents the input received by the agent.

Primary field:

- `question`

Pydantic validation guarantees that the question is not empty.

## ResearchResult

Represents information returned by a research tool.

Fields:

- `source`
- `content`

This separates tool output from the final response returned by the agent.

## ResearchResponse

Represents the structured result produced by the agent.

Fields:

- `answer`
- `sources`

These models provide explicit boundaries between input, tool results and agent output.

---

# 5. ResearchAgent

`ResearchAgent` is the main orchestration component.

Its responsibilities are:

- receive a `ResearchRequest`
- coordinate model-driven Tool Calling when configured
- coordinate the Decision Layer
- delegate execution to `ToolExecutor`
- transform a `ResearchResult` into a `ResearchResponse`

Its dependencies can be injected:

- `DecisionMaker`
- `ToolExecutor`
- `ToolCallingClient`

Default implementations preserve backwards compatibility with previous versions of the Research Agent.

The agent therefore orchestrates behaviour without directly depending on a concrete LLM provider or search implementation.

---

# 6. Evolution v0.1 — Basic Agent

Research Agent v0.1 introduced the minimum useful architecture.

The basic flow was conceptually:

    ResearchRequest
          │
          ▼
    ResearchAgent
          │
          ▼
       search()
          │
          ▼
    ResearchResult
          │
          ▼
    ResearchResponse

The objective was to understand basic orchestration before introducing additional abstractions.

---

# 7. Evolution v0.2 — Decision Layer

Research Agent v0.2 separated decision-making from orchestration.

The following concepts were introduced:

- `ResearchDecision`
- `DecisionMaker`
- `DeterministicDecisionMaker`

The flow became:

    ResearchRequest
          │
          ▼
    ResearchAgent
          │
          ▼
    DecisionMaker
          │
          ▼
    ResearchDecision
       /       \
    search     final

This removed the responsibility for deciding the next action from the agent itself.

---

# 8. ResearchDecision

`ResearchDecision` represents a high-level decision about what the agent should do.

Supported actions are currently:

- `search`
- `final`

The model enforces invariants:

- a `search` decision requires a query
- a `final` decision must not contain a query

This validation prevents invalid decision states from entering the orchestration layer.

---

# 9. DecisionMaker Protocol

`DecisionMaker` defines the contract:

    decide(question) -> ResearchDecision

The architecture currently contains two implementations.

## DeterministicDecisionMaker

Always produces a search decision.

It provides deterministic behaviour and preserves the earlier execution path.

## LLMDecisionMaker

Delegates the decision to a language model through `ModelClient`.

This allows the decision strategy to change without changing `ResearchAgent`.

---

# 10. Evolution v0.3 — LLM Decision Maker

Research Agent v0.3 introduced LLM-based decision-making.

Architecture:

    ResearchAgent
          │
          ▼
    DecisionMaker
          ▲
          │
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

The LLM produces a structured `ResearchDecision`.

At this stage, the LLM does not perform native Tool Calling.

It only decides whether the application should search or return a final result.

---

# 11. ModelClient Protocol

`ModelClient` defines the provider-independent contract for structured model generation.

Conceptually:

    generate(prompt, output_type) -> validated Pydantic model

This allows `LLMDecisionMaker` to depend on an abstraction rather than directly on the OpenAI SDK.

It also enables deterministic unit testing with fake model clients.

---

# 12. OpenAIModelClient

`OpenAIModelClient` is the current adapter between the application and the OpenAI Responses API.

In v0.4 it supports two related capabilities.

## Structured Outputs

Used by the M03 Decision Layer through:

`generate(...)`

The response is parsed into the requested Pydantic model.

## Native Tool Calling

Used by the M04 Tool Calling path through:

`request_tool_call(...)`

The same adapter therefore currently satisfies two application-level contracts:

- `ModelClient`
- `ToolCallingClient`

This is deliberate at the current scale of the project.

A separate provider adapter is not introduced until additional complexity provides a concrete reason for that abstraction.

---

# 13. Evolution v0.4 — Native Tool Calling

Research Agent v0.4 introduces native provider Function Calling.

The central execution path is:

    User Question
          │
          ▼
         LLM
          │
          │ native function_call
          ▼
       ToolCall
          │
          ▼
     ToolExecutor
          │
          ▼
      Search Tool
          │
          ▼
    ResearchResult
          │
          ▼
    ResearchResponse

This architecture separates three concepts that must not be confused:

**Tool definition**

Describes a capability that the model may request.

**Tool selection**

The model decides whether to request the tool and provides its arguments.

**Tool execution**

The application validates the request and executes the corresponding implementation.

The LLM does not execute Python functions directly.

---

# 14. ToolCallingClient Protocol

`ToolCallingClient` defines the application contract for requesting native tool calls.

Conceptually:

    request_tool_call(prompt) -> ToolCall | None

Returning `None` is valid.

It represents a model response that did not request an available tool.

This is particularly important because the current provider configuration allows automatic tool selection.

---

# 15. ToolCall

`ToolCall` represents a validated application-level request to execute a tool.

Current structure:

- `name`
- `arguments`

The only supported tool name in v0.4 is:

- `search`

This is intentionally narrow.

A generalized Tool Registry is not justified while the agent has only one tool.

---

# 16. SearchToolArguments

`SearchToolArguments` contains the validated arguments accepted by the search tool.

Current field:

- `query`

The query must be non-empty.

Provider arguments cross an explicit validation boundary:

    Provider function_call
          │
          ▼
    JSON arguments
          │
          ▼
    json.loads()
          │
          ▼
    SearchToolArguments
          │
          ▼
       ToolCall

This prevents unvalidated provider data from being passed directly into tool execution.

---

# 17. ToolExecutor

`ToolExecutor` is responsible for executing validated `ToolCall` objects.

The search implementation is injected as a dependency:

    ToolExecutor(search_tool=...)

This provides several benefits:

- separation between orchestration and implementation
- deterministic unit tests
- easy replacement of the search implementation
- no network dependency in the test suite

The current executor deliberately avoids a sophisticated registry or dispatch framework.

That abstraction will only become justified when multiple tools require it.

---

# 18. Search Tool

The current `search()` function is a simulated research tool.

It returns a `ResearchResult` with:

- a simulated source
- simulated content

This distinction is important:

**v0.4 implements real native Tool Calling at the model/provider boundary, but the underlying search implementation remains simulated.**

A real external search provider is not required to understand the Tool Calling architecture.

---

# 19. Decision vs Tool Call vs Tool Execution

These concepts represent different architectural responsibilities.

## ResearchDecision

A high-level application decision.

Example:

    action = "search"
    query = "Python 3.14 new features"

It answers:

**What should the agent do next?**

## ToolCall

A concrete request to invoke a specific capability.

Example:

    name = "search"
    arguments.query = "Python 3.14 new features"

It answers:

**Which tool should be invoked, and with which validated arguments?**

## Tool Execution

The actual application-controlled execution of the requested capability.

It answers:

**How is that validated request executed?**

Keeping these concepts separate prevents model decisions, provider messages and application execution from becoming tightly coupled.

---

# 20. Dependency Injection

Dependency Injection is used throughout the architecture.

Examples include:

- `ResearchAgent(decision_maker=...)`
- `ResearchAgent(tool_executor=...)`
- `ResearchAgent(tool_calling_client=...)`
- `LLMDecisionMaker(client=...)`
- `ToolExecutor(search_tool=...)`

This makes dependencies explicit and replaceable.

It also enables testing without:

- real API keys
- external network calls
- live search providers

---

# 21. Testing Architecture

The project uses deterministic automated tests as a core architectural constraint.

Current Project 01 test modules are:

    tests/project_01/
    ├── test_agent.py
    ├── test_decision.py
    ├── test_decision_maker.py
    ├── test_llm_decision_maker.py
    ├── test_models.py
    ├── test_openai_model_client.py
    ├── test_tool_call.py
    ├── test_tool_executor.py
    └── test_tools.py

There is also a repository-level test:

    tests/test_types.py

The current complete test suite contains:

**24 passing tests**

The test strategy uses fakes and injected dependencies so CI does not require OpenAI credentials or external services.

---

# 22. Provider Boundary Testing

`OpenAIModelClient` is tested with fake Responses API objects.

These tests validate application behaviour such as:

- structured response parsing
- missing structured output handling
- native `function_call` parsing
- tool schema transmission
- conversion into validated `ToolCall` objects

This tests the adapter contract without performing paid or network-dependent API calls.

---

# 23. Manual Integration Testing

A manual native Tool Calling smoke test was prepared against the real OpenAI API.

The request successfully reached the API service, but model inference could not be completed beca appropriate.

3. **Dependency Injection**
   External behaviour can be replaced by deterministic test doubles.

4. **Boundary validation**
   Provider-generated arguments are validated before execution.

5. **Incremental complexity**
   New abstractions are introduced only when required.

6. **Deterministic testing**
   Automated tests do not depend on API keys or network access.

7. **Provider isolation**
   OpenAI-specific behaviour remains concentrated in the provider adapter.

8. **Framework independence first**
   Fundamental agent concepts are implemented before introducing LangGraph.

---

# 28. Architecture Direction

The long-term objective is not to accumulate abstractions.

The objective is to evolve the architecture only when each new capability creates a concrete engineering requirement.

The progression is therefore:

    Basic Agent
        ↓
    Decision Layer
        ↓
    LLM Decision Maker
        ↓
    Tool Calling
        ↓
    Agent Loop & State
        ↓
    Planning
        ↓
    LangGraph
        ↓
    Memory
        ↓
    Evaluation & Observability
        ↓
    Production

Each stage should remain understandable, testable and traceable to the architectural problem it solves.
