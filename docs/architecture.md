# Architecture — RepoMind

## Philosophy

RepoMind follows **Clean Architecture** with **Hexagonal Architecture** (light) principles.

The core rule: **dependencies always point inward**.

```
interfaces / infrastructure
        ↓
    application
        ↓
      domain
        ↓
       core
```

The `domain` and `core` layers have **zero external dependencies**.

---

## Layer responsibilities

### `core/` — Abstractions
Abstract interfaces only. No business logic, no infrastructure.

| Interface | Role |
|---|---|
| `BaseLLM` | Contract for all LLM providers |
| `BaseRetriever` | Contract for all retrieval strategies |
| `BaseGraphStore` | Contract for all graph backends |
| `BaseAgent` | Contract for all agents |
| `BaseEmbeddingModel` | Contract for all embedding models |

### `domain/` — Business entities
Pure Python. No framework imports.

| Module | Contents |
|---|---|
| `models.py` | `CodeChunk`, `CodeNode`, `DependencyEdge`, `RetrievalResult` |
| `state.py` | `AgentState` (TypedDict for LangGraph) |
| `exceptions.py` | All custom exceptions |

### `infrastructure/` — Concrete implementations
All external dependencies live here.

| Package | Implementations |
|---|---|
| `llm/` | `OpenAIClient`, `OllamaClient`, `factory.py` |
| `vector/` | `ChromaVectorStore` |
| `graph/` | `NetworkXGraphStore`, `Neo4jGraphStore`, `factory.py` |
| `embedding/` | _(to be implemented)_ |

### `application/` — Use cases
Orchestrates domain + infrastructure. No HTTP, no framework specifics.

| Use case | Responsibility |
|---|---|
| `AnalyzeRepositoryUseCase` | Full ingestion pipeline |
| `AnswerQueryUseCase` | Query → agent workflow → answer |
| `GenerateImpactReportUseCase` | Impact analysis for a given change |

### `agents/` — Individual agents
Each agent has one responsibility, one input, one output.

| Agent | Responsibility |
|---|---|
| `PlannerAgent` | Decomposes the user query into steps |
| `RetrieverAgent` | Fetches relevant chunks from vector store |
| `GraphExplorerAgent` | Traverses the dependency graph |
| `AnalyzerAgent` | Performs structural / impact analysis |
| `SynthesizerAgent` | Produces the final answer |

### `workflows/` — LangGraph orchestration
Defines state transitions between agents. No business logic here.

### `retrieval/` — Retrieval strategies
Independent of agents. Pluggable strategies: vector, hybrid, graph-aware.

### `graph/` — Graph traversal logic
Dependency graph construction and traversal. Independent of agents.

### `analysis/` — Analysis logic
Impact analysis, architecture summarization, code smell detection.

---

## SOLID compliance

| Principle | How it's enforced |
|---|---|
| SRP | One class = one responsibility. No god objects. |
| OCP | New providers added via inheritance/adapters, not modifications. |
| LSP | All implementations are substitutable via base interfaces. |
| ISP | Interfaces are small and focused. |
| DIP | All services receive dependencies via `__init__` (injection), never instantiate them. |

---

## Anti-patterns (forbidden)

- `utils.py` catch-all files
- Business logic in API routes
- Circular imports between layers
- Hardcoded provider instantiation (`self.llm = OpenAIClient()`)
- Untyped dicts (`dict` without TypedDict or Pydantic)
- `print()` statements
- Bare `except Exception: pass`
- Inline prompts in agent code
- God-object agents doing everything
