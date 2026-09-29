# AI Agent Engineering

Professional AI Agent Engineering — agents, Tool Calling, RAG, MCP, evaluation and production engineering.

This repository is both a structured learning laboratory and a professional portfolio focused on understanding how modern AI agents are designed, implemented, tested and evolved.

## 🎯 Mission

Build practical, production-oriented AI agents while developing a solid understanding of:

- agent architectures
- Tool Calling
- Agent Loops and state
- planning
- LangGraph
- memory
- Retrieval-Augmented Generation (RAG)
- Model Context Protocol (MCP)
- multi-agent systems
- evaluation and testing
- observability
- deployment and production engineering

## 🧠 Learning Philosophy

> 80% building. 20% theory.

The development process follows:

**Understand → Design → Implement → Test → Review → Document**

Complexity is introduced incrementally.

Framework abstractions are added only after the underlying engineering concepts have been implemented and understood.

---

## 🚀 Current Status

### Project 01 — Research Agent

**Current version: v0.5 — Agent Loop & State**

Completed modules:

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

The complete progression is documented in:

`docs/roadmap.md`

---

## 🏗️ Research Agent Architecture

The Research Agent currently separates orchestration, execution state, model integration and tool execution.

    ResearchRequest
          │
          ▼
    ResearchAgent
          │
          ├──────────── AgentState
          │                 │
          │                 ├── observations
          │                 └── step_count
          │
          ├──────────── ModelSession
          │                 │
          │                 ├── ToolRequested
          │                 ├── FinalAnswer
          │                 └── OpenAIModelSession
          │
          └──────────── Tool Layer
                            │
                            ├── ToolCall
                            ├── SearchToolArguments
                            ├── ToolExecutor
                            └── search()

The architecture is intentionally incremental.

Research Agent v0.5 adds a controlled Agent Loop while keeping tool execution and loop policy under application control.

The Decision Layer and one-shot Tool Calling abstractions from previous versions remain available as compatibility paths.

---

## 🛠️ Tool Calling — v0.4

The current native Tool Calling path is:

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

The LLM requests a capability.

The application validates and executes the request.

The LLM does **not** execute Python functions directly.

The current search implementation remains simulated. Native Tool Calling and the implementation of the underlying tool are treated as separate concerns.

---

## 🔁 Agent Loop & State — v0.5

Research Agent v0.5 extends Tool Calling into controlled iterative execution:

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

Tool results are converted into observations and can influence subsequent model turns.

`OpenAIModelSession` keeps provider-specific continuation metadata such as `response_id` and `call_id` outside the provider-independent agent state.

Agent execution is bounded by `max_steps` to prevent uncontrolled Tool Calling loops.

The complete automated test suite currently contains **39 passing tests**.

---

## 🧩 Core Engineering Concepts

The project currently demonstrates:

- explicit request and response models
- Pydantic validation
- Decision Layer separation
- Python Protocols
- Dependency Injection
- provider adapters
- Structured Outputs
- native Function Calling
- typed Tool Calls
- provider boundary validation
- deterministic test doubles
- application-controlled tool execution
- explicit Agent State and observations
- iterative model sessions
- provider continuation isolation
- bounded Agent Loops with `max_steps`
- incremental architecture evolution

---

## 🧪 Testing

Automated tests are designed to remain deterministic and independent of external services.

The test suite does not require:

- OpenAI API credentials
- paid model inference
- network access
- live search providers

External behaviour is replaced with fakes or injected implementations where appropriate.

Current repository validation:

**24 tests passing**

Primary test command:

    pytest -q

Static analysis:

    ruff check .

---

## 🛠️ Technology Stack

### Core

- Python 3.14+
- Pydantic
- FastAPI

### AI Agent Engineering

- OpenAI API
- OpenAI Agents SDK
- LangGraph

### Knowledge and Retrieval

- Retrieval-Augmented Generation (RAG)
- Qdrant
- PostgreSQL

### Integration

- Model Context Protocol (MCP)
- APIs
- SQL
- external tools

### Engineering

- pytest
- Ruff
- Git
- GitHub
- GitHub Actions
- Docker

Not every technology listed above is used by the current Research Agent version.

The stack is introduced progressively according to the project roadmap.

---

## 📚 Projects

### 01 — Research Agent

Progressive research-oriented agent used to learn the fundamental architecture of AI agents.

Current capabilities include:

- structured request and response models
- deterministic and LLM-driven decisions
- Structured Outputs
- native Tool Calling
- validated tool arguments
- Dependency Injection
- application-controlled tool execution

The next evolution introduces **Agent Loop & State**.

### 02 — RAG Agent

Knowledge-grounded agent using document retrieval and vector search.

Planned areas include:

- document ingestion
- chunking
- embeddings
- Qdrant
- retrieval
- retrieval evaluation

### 03 — MCP Agent

Agent connected to external capabilities through the Model Context Protocol.

### 04 — Multi-Agent System

Multiple specialist agents collaborating on more complex workflows.

---

## 📁 Repository Structure

    ai-agent-engineering/
    ├── docs/
    │   ├── architecture.md
    │   ├── learning-log.md
    │   └── roadmap.md
    ├── examples/
    ├── projects/
    │   ├── 01_research_agent/
    │   ├── 02_rag_agent/
    │   ├── 03_mcp_agent/
    │   └── 04_multi_agent/
    ├── src/
    │   └── agents/
    ├── tests/
    │   └── project_01/
    ├── .env.example
    ├── .gitignore
    ├── LICENSE
    ├── pyproject.toml
    └── README.md

---

## 📖 Documentation

### Architecture

`docs/architecture.md`

Describes the current architecture, component responsibilities, architectural evolution and deliberate boundaries.

### Roadmap

`docs/roadmap.md`

Defines the progression from M00 through Research Agent v1.0 and the subsequent RAG, MCP and Multi-Agent projects.

### Learning Log

`docs/learning-log.md`

Records what was implemented and learned during each module, including architectural decisions, testing strategy and deliberately postponed concepts.

---

## 🧭 Engineering Principles

The project follows several core principles:

1. **Architecture before frameworks**
   Understand the underlying mechanism before delegating it to a framework.

2. **Explicit boundaries**
   Requests, decisions, Tool Calls, tool results and responses use explicit models.

3. **Dependency Injection**
   External behaviour remains replaceable and testable.

4. **Boundary validation**
   Provider-generated data is validated before execution.

5. **Deterministic testing**
   CI should not require API keys, paid inference or network access.

6. **Incremental complexity**
   New abstractions are introduced only when they solve a concrete engineering problem.

7. **Provider isolation**
   Provider-specific API behaviour remains separated from core application logic.

---

## 🔜 Next Step

### M06 — Planning

Research Agent v0.6 will introduce explicit planning and decomposition of complex tasks.

The next architectural progression is:

    User Goal
       │
       ▼
      Plan
       │
       ▼
    Task Steps
       │
       ▼
    Controlled Execution
       │
       ▼
    Replanning when required
       │
       ▼
    Final Answer

M06 will focus on task decomposition, explicit plans, plan execution and controlled replanning.

LangGraph remains deliberately postponed until M07, after the underlying Planning concepts are understood independently.

---

## 👤 Author

**Fernando Silva**

Technical learning and experimentation project focused on professional AI Agent Engineering.
