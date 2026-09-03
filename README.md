# AI Agent Engineering

Professional AI Agent Engineering — agents, tools, RAG, MCP, evaluation and production.

## 🎯 Mission

Build practical, production-oriented AI agents while developing a solid understanding of:

- Agent architectures
- Tool calling
- Agent workflows
- Retrieval-Augmented Generation (RAG)
- Model Context Protocol (MCP)
- Multi-agent systems
- Memory and state
- Evaluation and testing
- Observability
- Deployment and production engineering

This repository is both a learning laboratory and a professional portfolio.

## 🧠 Learning Philosophy

> 80% building. 20% theory.

Every major concept follows:

**Theory → Implementation → Tests → Documentation → Git**

## 🏗️ Architecture

The project progressively evolves from simple agents to production systems:

```text
User
  │
  ▼
Agent / API
  │
  ├── Tools
  ├── Memory
  ├── RAG
  ├── Workflows
  ├── MCP
  └── Other Agents
        │
        ▼
    Evaluation
        │
        ▼
   Observability
        │
        ▼
    Production 
🛠️ Technology Stack
Core
Python 3.14+
Pydantic
FastAPI
Agent Engineering
OpenAI Agents SDK
LangGraph
Knowledge
Retrieval-Augmented Generation (RAG)
Qdrant
PostgreSQL
Integration
Model Context Protocol (MCP)
APIs
SQL
External tools
Engineering
pytest
Ruff
GitHub Actions
Docker
📚 Project Roadmap
| Level | Focus       | Status |
| ----- | ----------- | ------ |
| L1    | Basic Agent | 🔜     |
| L2    | Tools       | 🔜     |
| L3    | RAG         | 🔜     |
| L4    | MCP         | 🔜     |
| L5    | Multi-Agent | 🔜     |
| L6    | Evaluation  | 🔜     |
| L7    | Production  | 🔜     |

🚀 Projects
01 — Research Agent

A research-oriented agent capable of:

Understanding a research request
Planning the investigation
Using external tools
Collecting evidence
Synthesising information
Producing a structured answer
02 — RAG Agent

Knowledge-grounded agent using documents and vector search.

03 — MCP Agent

Agent connected to external capabilities through Model Context Protocol.

04 — Multi-Agent System

Orchestrated specialist agents solving a complex business problem.

📁 Repository Structure
ai-agent-engineering/
├── docs/
├── examples/
├── projects/
│   ├── 01_research_agent/
│   ├── 02_rag_agent/
│   ├── 03_mcp_agent/
│   └── 04_multi_agent/
├── src/
│   └── agents/
│       ├── core/
│       ├── tools/
│       ├── rag/
│       ├── workflows/
│       └── evaluation/
├── tests/
├── .env.example
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
👤 Author

Fernando Silva

Technical learning and experimentation project focused on professional AI Agent Engineering.
