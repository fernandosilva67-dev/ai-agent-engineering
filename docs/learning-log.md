# AI Agent Engineering — Learning Log

This document records the practical learning progression of the AI Agent Engineering project.

It is not intended to be a conventional changelog.

For each module, it records:

- what was built
- why the architecture changed
- the engineering concepts learned
- how the implementation was validated
- what was deliberately postponed to a later module

The development method is:

**Understand → Design → Implement → Test → Review → Document**

---

# M00 — Environment & Git

## Objective

Create a professional development foundation before implementing AI agent functionality.

## Work completed

The repository and development workflow were established with:

- Python 3.14+
- virtual environment
- `pyproject.toml`
- pytest
- Ruff
- Git
- GitHub
- branch-based development
- Pull Request workflow
- environment configuration

Initial project bootstrap:

`8a84fc9 — chore: bootstrap AI agent engineering project`

Merged through Pull Request #1.

## What I learned

The repository is part of the architecture.

Before implementing an agent, the project needs repeatable dependency management, tests, source control and clear separation between source code, projects and documentation.

Git is not only a backup mechanism. Branches, commits and Pull Requests provide a traceable engineering history.

---

# M01 — Basic Agent

**Target:** Research Agent v0.1

## Objective

Build the smallest useful Research Agent before introducing LLM orchestration or frameworks.

## Work completed

Main implementation:

`3e01c6b — feat: implement basic research agent`

Merged through Pull Request #2.

The first version introduced:

- `ResearchAgent`
- `ResearchRequest`
- `ResearchResult`
- `ResearchResponse`
- a simulated `search()` tool
- unit tests

## Architecture

The initial flow was intentionally simple:

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

## What I learned

An agent can first be understood as an orchestrator.

The basic responsibilities are:

1. receive structured input
2. invoke a capability
3. receive a result
4. return structured output

Pydantic models establish explicit boundaries between those stages.

## Deliberately postponed

The module did not introduce:

- LLM decision-making
- native Tool Calling
- Agent Loop
- state
- planning
- memory
- LangGraph

The objective was to understand the minimum architecture first.

---

# M02 — Decision Layer

**Target:** Research Agent v0.2

## Objective

Separate the question:

**What should the agent do?**

from:

**How does the agent execute that action?**

## Work completed

Main commits:

`1066321 — refactor: separate research decision logic`

`9b44d56 — fix: enforce research decision invariants`

Merged through Pull Request #3.

The module introduced:

- `ResearchDecision`
- `DecisionMaker` Protocol
- `DeterministicDecisionMaker`
- Dependency Injection for decision behaviour
- decision invariants

## Architecture

The flow evolved to:

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

## What I learned

Decision-making is a separate responsibility from orchestration.

The `ResearchAgent` should not need to know how a decision is produced.

A Protocol allows the agent to depend on a contract instead of a concrete implementation.

This enables different decision strategies without changing the orchestration layer.

## Decision invariants

`ResearchDecision` enforces valid states:

- `search` requires a query
- `final` cannot contain a query

This demonstrated an important principle:

**Invalid states should be rejected at the model boundary rather than handled throughout the application.**

## Deliberately postponed

The decision mechanism remained deterministic.

An LLM was not yet required to understand the Decision Layer itself.

---

# M03 — LLM Decision Maker

**Target:** Research Agent v0.3

## Objective

Replace deterministic decision-making with an optional LLM-driven strategy while preserving the existing architecture.

## Work completed

Main commits:

`02ae273 — chore: normalize line endings and formatting`

`cf0d520 — feat: add LLM-powered research decisions`

`068afb8 — docs: document research agent v0.3`

Merged through Pull Request #4.

The module introduced:

- `LLMDecisionMaker`
- `ModelClient` Protocol
- `OpenAIModelClient`
- OpenAI Responses API integration
- Structured Outputs
- fake model clients for deterministic testing

## Architecture

The architecture evolved to:

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

## What I learned

An LLM should be treated as an external dependency.

Application logic should not be tightly coupled to a specific SDK or provider.

`ModelClient` creates an application-level boundary between the Decision Layer and the provider adapter.

Structured Outputs allow model responses to be converted into validated application models rather than relying on unstructured text parsing.

## Testing lesson

Automated tests should not require:

- API keys
- paid inference
- network access
- provider availability

Fake clients make the core architecture deterministic and suitable for CI.

Real API calls are useful as manual integration tests, but they are not substitutes for automated unit tests.

## Important architectural boundary

M03 uses the LLM to produce a structured `ResearchDecision`.

It does **not** use native provider Function Calling.

That distinction is intentional:

    Structured Decision
            ≠
    Native Tool Calling

Native Tool Calling belongs to M04.

## Deliberately postponed

M03 did not introduce:

- native Function Calling
- Tool Executor abstraction
- Agent Loop
- repeated model/tool interaction
- state
- planning
- memory
- LangGraph

---

# M04 — Tool Calling

**Target:** Research Agent v0.4

## Objective

Introduce native model Tool Calling while keeping tool execution under application control.

The central objective was to understand the difference between:

- defining a tool
- allowing the model to select a tool
- validating a tool request
- executing the tool

This module deliberately implements a single tool execution rather than a complete Agent Loop.

## Work completed

Main commits:

`ff2c7e0 — feat: add native tool calling infrastructure`

`c8e2a36 — feat: integrate model tool calls with research agent`

The module introduced:

- `SearchToolArguments`
- `ToolCall`
- `ToolCallingClient`
- `ToolExecutor`
- native OpenAI Function Calling
- provider argument parsing
- Pydantic boundary validation
- Dependency Injection for tool implementations
- integration of model-requested tool calls with `ResearchAgent`

## Architecture

The native Tool Calling path is:

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

The LLM requests an action.

The application remains responsible for validating and executing that action.

## Tool definition

The OpenAI provider receives a function definition describing the available `search` tool.

The definition contains:

- tool type
- function name
- description
- JSON Schema parameters
- required arguments
- strict schema configuration

The model receives the description of the capability.

It does not receive direct control over the Python function.

## Tool selection

The provider can return a native `function_call`.

The current implementation uses automatic tool selection.

Therefore, a tool request is optional and:

`request_tool_call(...)`

returns:

`ToolCall | None`

A `None` result means that the model did not request the available tool.

## Provider boundary validation

Provider arguments arrive as JSON.

The application converts them through the following boundary:

    function_call.arguments
             │
             ▼
         json.loads()
             │
             ▼
    SearchToolArguments
             │
             ▼
          ToolCall

`SearchToolArguments` is a Pydantic model.

The search query must be non-empty.

This ensures that provider-generated arguments are validated before application execution.

## Tool execution

`ToolExecutor` receives an already validated `ToolCall`.

The search implementation is injected:

    ToolExecutor(search_tool=...)

This means that the executor does not depend directly on a live search provider.

During automated tests, a fake search function can be injected.

## What I learned

### 1. Tool Calling does not mean the LLM executes code

The LLM does not invoke arbitrary Python code directly.

It produces a structured request describing the function it wants the application to invoke.

The application decides how that request is validated and executed.

### 2. Tool definition, selection and execution are different responsibilities

A tool can be available without being selected.

A selected tool still needs validated arguments.

A validated Tool Call still requires application-controlled execution.

Keeping these stages separate creates a safer and more testable architecture.

### 3. ResearchDecision and ToolCall are different concepts

`ResearchDecision` represents a high-level application decision.

For example:

    action = "search"
    query = "Python 3.14 new features"

`ToolCall` represents a concrete request for a particular capability.

For example:

    name = "search"
    arguments.query = "Python 3.14 new features"

Therefore:

    ResearchDecision
           ≠
       ToolCall
           ≠
    Tool Execution

This distinction prevents decision logic, provider protocol and execution logic from becoming tightly coupled.

### 4. Provider output is untrusted boundary data

Even when the provider supports strict schemas, application-side validation remains useful.

Provider arguments are therefore converted into typed Pydantic models before execution.

### 5. Dependency Injection simplifies testing

The executor receives the search implementation rather than creating it internally.

This allows tests to replace external behaviour with deterministic fakes.

## OpenAIModelClient evolution

`OpenAIModelClient` now supports two capabilities.

From M03:

`generate(...)`

for Structured Outputs.

From M04:

`request_tool_call(...)`

for native Function Calling.

The adapter therefore currently satisfies the application requirements of both:

- `ModelClient`
- `ToolCallingClient`

A second provider adapter was not introduced because the current complexity does not justify it.

## ResearchAgent integration

`ResearchAgent` now optionally receives:

`tool_calling_client`

When configured, the agent first requests a model Tool Call.

If the model requests a tool:

    ToolCallingClient
          │
          ▼
       ToolCall
          │
          ▼
     ToolExecutor
          │
          ▼
    ResearchResult

If no Tool Call is returned, the existing Decision Layer remains available as a fallback.

This preserves the previous architecture while adding the new capability incrementally.

## Testing

The Tool Calling implementation is covered by deterministic tests.

Tests validate:

- typed tool arguments
- rejection of empty search queries
- Tool Call construction
- Tool Executor dispatch
- Dependency Injection
- native provider `function_call` parsing
- tool schema transmission
- integration with `ResearchAgent`

At the end of the implementation:

**24 tests passed in the complete repository test suite.**

Ruff also completed successfully.

## Manual API smoke test

A manual integration test was attempted using the real OpenAI API.

The purpose was to validate:

    OpenAI API
         │
         ▼
    native function_call
         │
         ▼
    OpenAIModelClient
         │
         ▼
    validated ToolCall

The request reached the OpenAI API, but inference was not executed because the API account had no remaining credits.

The provider returned:

    HTTP 429
    code: credit_balance_exhausted

This was an external billing condition rather than an application failure.

No code change was made in response to this error.

The real native `function_call` smoke test can be repeated when API credits are available.

## Important distinction

The project now implements **real native Tool Calling at the model/provider boundary**.

However, the underlying `search()` implementation remains simulated.

Therefore:

    Native Tool Calling     → real provider mechanism
    Search implementation   → simulated application tool

These are independent concerns.

A live search provider is not required to understand or test the Tool Calling architecture.

## Deliberately postponed

M04 does not implement:

- Agent Loop
- repeated model/tool interactions
- model continuation after tool execution
- `function_call_output`
- persistent execution state
- planning
- memory
- LangGraph
- sophisticated Tool Registry
- multiple tools
- multi-agent orchestration

These capabilities are outside the scope of Research Agent v0.4.

## Next step

M05 introduces:

**Agent Loop & State**

The architecture will evolve from:

    question
       ↓
    model
       ↓
     tool
       ↓
    result

to controlled iterative execution:

    decide
       ↓
     tool
       ↓
    observe
       ↓
    decide
       ↓
     tool
       ↓
      ...
       ↓
     final

This will introduce execution state, observations, model continuation, termination conditions and controlled iteration limits.

The key principle remains the same:

**Introduce the next abstraction only after the previous mechanism is understood, implemented and tested.**

---

# M05 — Agent Loop & State

Research Agent v0.5 introduces the first controlled iterative Agent Loop.

The objective of this module was not to introduce LangGraph or a planning framework.

The objective was to understand and implement the underlying execution mechanics directly:

    decide
       ↓
     tool
       ↓
    observe
       ↓
    decide
       ↓
      ...
       ↓
     final

## Architectural problem

In v0.4, native Tool Calling ended after one tool execution:

    Model
      ↓
    ToolCall
      ↓
    ToolExecutor
      ↓
    ResearchResult
      ↓
    ResearchResponse

That architecture cannot support an agent that needs to use the result of a tool before deciding what to do next.

v0.5 therefore changes the meaning of a tool result.

A `ResearchResult` is no longer automatically the final answer.

Instead:

    ResearchResult
         ↓
    Observation
         ↓
     AgentState
         ↓
    next model turn

This creates the feedback loop required for iterative agent execution.

## AgentState

`AgentState` was introduced to represent provider-independent execution state.

It currently contains:

- `question`
- `observations`
- `step_count`

The state is intentionally small.

It does not contain:

- OpenAI client objects
- model configuration
- prompts
- tools
- `response_id`
- `call_id`
- `max_steps`

This established an important design rule:

**agent execution state and provider continuation state are different concerns.**

## Observation

`Observation` represents what the agent learns after a tool has been executed.

It contains:

- `tool_name`
- `source`
- `content`

The execution flow is therefore:

    ToolRequested
         ↓
    ToolExecutor
         ↓
    ResearchResult
         ↓
    Observation
         ↓
    AgentState

Sources in the final `ResearchResponse` are derived from accumulated observations rather than duplicated in the state.

## ModelTurnResult

A model interaction can now produce two provider-independent outcomes:

    ModelTurnResult
    ├── ToolRequested
    │      └── ToolCall
    │
    └── FinalAnswer
           └── answer

This makes termination explicit.

`ToolRequested` means that the application must execute a tool and continue the interaction.

`FinalAnswer` means that the Agent Loop can terminate.

## ModelSession

A new `ModelSession` Protocol defines iterative model interaction:

    start(question) -> ModelTurnResult

    continue_with(observation) -> ModelTurnResult

This abstraction was introduced because iterative model execution requires continuation state.

That state should not leak into the generic `ResearchAgent`.

The Agent Loop therefore works with a provider-independent `ModelSession`.

## OpenAIModelSession

`OpenAIModelSession` implements the session contract for the OpenAI Responses API.

The adapter maintains the provider-specific values:

- `response_id`
- `call_id`

When OpenAI requests a function call:

    OpenAI response
         ↓
    function_call
         ↓
    call_id
         ↓
    ToolRequested

The application executes the tool.

The resulting observation is then returned to the provider using:

    function_call_output

with the corresponding:

    call_id

The next request continues the provider interaction using:

    previous_response_id

This allows the model to inspect the tool result and either request another tool or produce the final answer.

## Provider boundary

A major architectural lesson from M05 is that provider orchestration metadata should remain at the provider boundary.

The following remain provider-independent:

- `AgentState`
- `Observation`
- `ToolCall`
- `ToolRequested`
- `FinalAnswer`
- `ResearchResponse`

OpenAI-specific continuation details remain inside `OpenAIModelSession`.

This avoids coupling the core agent architecture to one model provider.

## Agent Loop

When a `ModelSession` is configured, `ResearchAgent` now performs the controlled loop:

    create AgentState
          ↓
    ModelSession.start()
          ↓
      model turn
          ↓
       ┌──┴───────────────┐
       │                  │
 ToolRequested       FinalAnswer
       │                  │
       ↓                  ↓
 ToolExecutor       ResearchResponse
       │
       ↓
 Observation
       │
       ↓
 update AgentState
       │
       ↓
 ModelSession.continue_with()
       │
       └──────────────► next model turn

The loop remains explicit Python code.

LangGraph is deliberately postponed until M07 so that the underlying mechanics are understood before introducing a graph orchestration framework.

## Loop safety

Iterative agents require explicit execution limits.

`ResearchAgent` therefore introduces:

    max_steps

The current default is:

    max_steps = 5

The limit counts tool executions.

Before executing an additional requested tool, the agent checks whether the configured limit has already been reached.

If so, execution terminates with a `RuntimeError`.

This protects the application from uncontrolled or infinite Tool Calling loops.

`max_steps` belongs to `ResearchAgent` rather than `AgentState` because it is execution policy, not accumulated execution state.

## Backward compatibility

The previous execution paths remain available.

The current priority is:

    ModelSession
        ↓
    ToolCallingClient
        ↓
    DecisionMaker

This allows the architecture to evolve incrementally without deleting the mechanisms introduced in earlier modules.

The older abstractions remain useful for understanding the progression from deterministic decisions to native Tool Calling and finally to iterative execution.

## Testing

M05 added deterministic tests for:

- `AgentState`
- `Observation`
- `ToolRequested`
- `FinalAnswer`
- repeated Tool Calls
- observation accumulation
- final answer termination
- source derivation
- `max_steps`
- OpenAI Tool Call parsing
- `response_id`
- `call_id`
- `function_call_output`
- provider continuation
- invalid session continuation
- complete ResearchAgent/OpenAIModelSession/ToolExecutor integration

The integration test uses fake OpenAI responses and a fake search implementation.

This validates the complete orchestration path without requiring:

- an API key
- network access
- provider credits

At the end of M05:

**39 tests passed in the complete repository test suite.**

Ruff also completed successfully.

## Deliberately postponed

M05 does not introduce:

- Planning
- task decomposition
- replanning
- LangGraph
- Memory
- sophisticated Tool Registry
- parallel Tool Calls
- multi-agent orchestration

These capabilities are outside the scope of Research Agent v0.5.

## Key lessons

The main lessons from M05 are:

1. A Tool Call is not the end of an agent interaction.
2. A tool result becomes an observation that can influence the next model turn.
3. Agent state and provider continuation state should remain separate.
4. Provider-specific identifiers should remain behind the provider adapter.
5. Agent loops require explicit termination semantics.
6. Agent loops require bounded execution.
7. External systems can be tested deterministically with fakes.
8. Frameworks should be introduced only after the mechanisms they abstract are understood.

## Next step

M06 introduces:

**Planning — Research Agent v0.6**

The next architectural problem is no longer simply:

    What should I do next?

It becomes:

    How should I decompose and execute a multi-step task?

Planning will introduce explicit task decomposition and controlled plan execution without yet introducing LangGraph.

---

# Current Learning Status

Project 01 has progressed through:

| Module | Version | Capability | Status |
|---|---|---|---|
| M00 | — | Environment & Git | ✅ Completed |
| M01 | v0.1 | Basic Agent | ✅ Completed |
| M02 | v0.2 | Decision Layer | ✅ Completed |
| M03 | v0.3 | LLM Decision Maker | ✅ Completed |
| M04 | v0.4 | Tool Calling | ✅ Completed |
| M05 | v0.5 | Agent Loop & State | ✅ Completed |
| M06 | v0.6 | Planning | ⏳ Next |

Current automated validation:

**39 tests passing**

Current development branch:

`feat/01-research-agent-v05-agent-loop`
