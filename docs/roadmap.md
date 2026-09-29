# AI Agent Engineering — Roadmap

This roadmap defines the progressive development path for the AI Agent Engineering repository.

The learning strategy is based on incremental engineering:

**Understand → Design → Implement → Test → Review → Document**

Each module introduces a limited set of concepts while preserving the architecture and tests from previous versions.

---

## Project 01 — Research Agent

The Research Agent evolves incrementally from a basic deterministic agent into a production-oriented AI agent.

| Module | Version | Focus | Status |
|---|---|---|---|
| M00 | — | Environment & Git | ✅ Completed |
| M01 | v0.1 | Basic Agent | ✅ Completed |
| M02 | v0.2 | Decision Layer | ✅ Completed |
| M03 | v0.3 | LLM Decision Maker | ✅ Completed |
| M04 | v0.4 | Tool Calling | ✅ Completed |
| M05 | v0.5 | Agent Loop & State | ✅ Completed |
| M06 | v0.6 | Planning | ⏳ Planned |
| M07 | v0.7 | LangGraph | ⏳ Planned |
| M08 | v0.8 | Memory | ⏳ Planned |
| M09 | v0.9 | Evaluation & Observability | ⏳ Planned |
| M10 | v1.0 | Production | ⏳ Planned |

---

## M00 — Environment & Git

Prepare the engineering environment and establish the Git workflow used throughout the course.

Topics include:

- Python development environment
- virtual environments
- Git and GitHub
- branch-based development
- commits and Pull Requests
- repository structure
- automated testing and linting foundations

---

## M01 — Basic Agent

**Target:** Research Agent v0.1

Introduce the minimum agent architecture.

Main concepts:

- request and response models
- basic agent orchestration
- tool invocation
- Pydantic models
- unit testing

---

## M02 — Decision Layer

**Target:** Research Agent v0.2

Separate decision-making from agent orchestration.

Main concepts:

- `ResearchDecision`
- `DecisionMaker` Protocol
- deterministic decision strategy
- Dependency Injection
- architectural separation of responsibilities
- decision invariants

---

## M03 — LLM Decision Maker

**Target:** Research Agent v0.3

Introduce an LLM as a decision-making component without introducing an Agent Loop.

Main concepts:

- `LLMDecisionMaker`
- `ModelClient` Protocol
- `OpenAIModelClient`
- OpenAI Responses API
- Structured Outputs
- provider adapter pattern
- fake model clients for deterministic tests

The model decides whether external research is required, but tool execution remains controlled by the application.

---

## M04 — Tool Calling

**Target:** Research Agent v0.4

Introduce native model Tool Calling.

Main concepts:

- native function calling
- tool definition
- tool selection
- tool execution
- typed tool arguments
- Pydantic boundary validation
- `ToolCall`
- `ToolCallingClient`
- `ToolExecutor`
- Dependency Injection for tool implementations

### Execution path

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

The LLM requests a tool invocation.

The application validates and executes that request.

The LLM does **not** execute Python functions directly.

### Deliberate limitation

Research Agent v0.4 performs a single tool execution.

It does not yet implement the iterative execution model:

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

That orchestration belongs to M05.

---

## M05 — Agent Loop & State

**Target:** Research Agent v0.5

Introduce controlled iterative agent execution.

Implemented concepts:

- Agent Loop
- `AgentState`
- `Observation`
- `ModelTurnResult`
- `ToolRequested`
- `FinalAnswer`
- `ModelSession` Protocol
- `OpenAIModelSession`
- model continuation after tool execution
- `function_call_output`
- provider continuation using `response_id` and `call_id`
- explicit termination with `FinalAnswer`
- controlled iteration using `max_steps`
- deterministic offline testing of the complete loop

### Execution path

    Question
       │
       ▼
    AgentState
       │
       ▼
    ModelSession
       │
       ├── FinalAnswer ─────────────► ResearchResponse
       │
       └── ToolRequested
                │
                ▼
           ToolExecutor
                │
                ▼
           Observation
                │
                ▼
        update AgentState
                │
                ▼
    ModelSession.continue_with()
                │
                └───────────────────► next model turn

Tool results are observations rather than automatic final answers.

The application remains responsible for tool execution and loop control, while provider-specific continuation state remains isolated inside the model adapter.

The complete automated test suite contains **39 passing tests**.

---

## M06 — Planning

**Target:** Research Agent v0.6

Introduce explicit planning and decomposition of complex tasks.

Planned concepts include:

- task decomposition
- explicit plans
- multi-step reasoning workflows
- plan execution
- controlled replanning

---

## M07 — LangGraph

**Target:** Research Agent v0.7

Represent agent workflows using LangGraph after the underlying Agent Loop and state concepts are understood independently.

Planned concepts include:

- graphs
- nodes
- edges
- state transitions
- conditional routing
- workflow orchestration

---

## M08 — Memory

**Target:** Research Agent v0.8

Introduce controlled short-term and persistent memory mechanisms.

Planned concepts include:

- conversational memory
- execution memory
- persistence
- memory boundaries
- memory retrieval

---

## M09 — Evaluation & Observability

**Target:** Research Agent v0.9

Introduce systematic evaluation, tracing, metrics and observability.

Planned concepts include:

- evaluation datasets
- deterministic tests
- LLM evaluation
- tracing
- metrics
- debugging agent executions
- observability

---

## M10 — Production

**Target:** Research Agent v1.0

Prepare the Research Agent for production-oriented deployment.

Topics will include:

- reliability
- configuration
- security
- error handling
- operational concerns
- deployment
- production architecture

---

# Subsequent Projects

After Research Agent v1.0, the course expands into specialized agent architectures.

---

## Project 02 — RAG Agent

Knowledge-grounded agent using document retrieval and vector search.

Primary concepts and technologies:

- Retrieval-Augmented Generation (RAG)
- embeddings
- Qdrant
- document ingestion
- chunking
- retrieval
- retrieval evaluation

---

## Project 03 — MCP Agent

Agent integrating external capabilities through the Model Context Protocol (MCP).

Primary concepts include:

- MCP architecture
- MCP clients
- MCP servers
- tools and resources
- external capability integration

---

## Project 04 — Multi-Agent System

Multiple specialist agents collaborating on more complex workflows.

Primary concepts include:

- specialist agents
- delegation
- coordination
- agent-to-agent workflows
- orchestration
- multi-agent architecture

---

# Engineering Principles

New abstractions are introduced only when the architecture requires them.

In particular:

- no Agent Loop before M05
- no Planning before M06
- no LangGraph before M07
- no Memory before M08
- no sophisticated Tool Registry until multiple tools justify it

The objective is not merely to use agent frameworks.

The objective is to understand the engineering principles those frameworks implement and to build each abstraction progressively.
