# Setup Guide — RepoMind

## Prerequisites

- Docker >= 24.0
- Docker Compose >= 2.20
- Git

No local Python installation required — everything runs in Docker.

---

## First-time setup

```bash
# 1. Clone the repository
git clone https://github.com/your-org/repomind
cd repomind

# 2. Copy and configure environment
cp .env.example .env
# Open .env and set your values (see Configuration section below)

# 3. Build and start
make install
make run
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

---

## Configuration

Edit `.env` before starting:

### With OpenAI (default)

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
GRAPH_BACKEND=networkx
```

### With Ollama (local, no API key needed)

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
GRAPH_BACKEND=networkx
```

Then start with:
```bash
make run-ollama
```

---

## Common commands

```bash
make run         # Start the stack
make stop        # Stop everything
make test        # Run tests
make lint        # Ruff lint
make format      # Black + isort
make typecheck   # mypy
make shell       # Shell inside the container
make logs        # Tail all logs
make clean       # Full reset (containers + volumes)
```

---

## Validation checklist

A correct setup means:

- [ ] `http://localhost:8000/health` returns `{"status": "ok"}`
- [ ] `http://localhost:8000/docs` loads the Swagger UI
- [ ] ChromaDB reachable at `http://localhost:8001`
- [ ] `make test` passes with no errors
- [ ] `make lint` returns no violations

---

## Troubleshooting

**Port already in use**
```bash
# Check what's using port 8000
lsof -i :8000
```

**ChromaDB not ready**
The app waits for ChromaDB's healthcheck. If it keeps failing:
```bash
docker compose logs chromadb
```

**OpenAI auth error**
Verify `OPENAI_API_KEY` is set correctly in `.env` (not `.env.example`).

**Full reset**
```bash
make clean
make run
```
