# RepoMind

> Agentic codebase understanding system — comprehend a Python repository like a senior developer.

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What is RepoMind?

RepoMind is **not** a chatbot. It is a structured agentic system that understands codebases through:

- **Structural parsing** — AST-aware chunking of Python source code
- **Dependency graph** — imports, classes, functions, call relationships
- **Vector retrieval** — semantic search over code chunks
- **Multi-agent reasoning** — planner, retriever, graph explorer, analyzer, synthesizer
- **Impact analysis** — understand what breaks when you change X

---

## Quickstart

```bash
git clone https://github.com/your-org/repomind
cd repomind

# Configure environment
cp .env.example .env
# Edit .env — set LLM_PROVIDER and your API key

# Launch (app + ChromaDB)
make run

# Or with local Ollama LLM
make run-ollama
```

API available at: `http://localhost:8000`
Docs at: `http://localhost:8000/docs`

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| Agents / Workflows | LangGraph |
| Vector DB | ChromaDB |
| Graph | NetworkX (dev) / Neo4j (prod) |
| LLM | Groq (default, free) / OpenAI / Ollama (local) |
| Parsing | Tree-sitter / AST |
| Config | Pydantic Settings |
| Logging | structlog |

---

## Architecture

```
app/
├── core/          # Abstract interfaces (BaseLLM, BaseAgent, ...)
├── domain/        # Business entities, state, exceptions
├── infrastructure/# Concrete implementations (OpenAI, Chroma, NetworkX)
├── application/   # Use cases
├── agents/        # Individual agents (Planner, Retriever, ...)
├── workflows/     # LangGraph orchestration
├── ingestion/     # Repository parsing & indexing
├── retrieval/     # Vector + hybrid retrieval
├── graph/         # Dependency graph traversal
├── analysis/      # Impact & architecture analysis
└── interfaces/    # API (FastAPI) and CLI
```

See [`docs/architecture.md`](docs/architecture.md) for the full architecture guide.

---

## Development commands

```bash
make install     # Build Docker images
make run         # Start full stack
make test        # Run tests
make lint        # Lint with ruff
make format      # Format with black + isort
make typecheck   # Type check with mypy
make check       # lint + typecheck
make shell       # Shell in app container
make clean       # Remove containers + cache
```

---

## LLM Providers

Switch providers via `.env` — no code changes needed.

**OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```

**Ollama (local):**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
```
Then run with `make run-ollama`.

---

## Graph Backends

```env
# Local (default, no extra setup)
GRAPH_BACKEND=networkx

# Persistent (production)
GRAPH_BACKEND=neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_PASSWORD=your_password
```

---

## MVP Scope (v1)

- [x] Project structure & architecture
- [x] Core abstractions
- [x] Domain models & state
- [x] Infrastructure (OpenAI, Ollama, ChromaDB, NetworkX, Neo4j)
- [x] Docker environment
- [ ] Repository ingestion pipeline
- [ ] Dependency graph construction
- [ ] Agent implementations
- [ ] LangGraph workflows
- [ ] CLI interface
- [ ] Impact analysis

---

## Docs

- [`docs/architecture.md`](docs/architecture.md) — Architecture decisions
- [`docs/setup.md`](docs/setup.md) — Full setup guide
- [`docs/roadmap.md`](docs/roadmap.md) — Roadmap & future work
- [`docs/agents.md`](docs/agents.md) — Agent contracts
- [`docs/graph_model.md`](docs/graph_model.md) — Graph data model
- [`docs/retrieval.md`](docs/retrieval.md) — Retrieval strategies

---

## LLM Providers

Switch providers via `.env` — no code changes needed.

**Groq (default — free, recommended):**
```env
LLM_PROVIDER=groq
GROQ_API_KEY=gsk_...        # Free key at console.groq.com
GROQ_MODEL=llama-3.3-70b-versatile
```

**OpenAI:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```

**Ollama (local, no API key):**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
```
Then: `make run-ollama`
