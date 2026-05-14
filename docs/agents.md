# Agents — RepoMind

Each agent has **one responsibility**, reads specific `AgentState` fields, and writes specific fields.
No agent may read or write fields outside its contract.

---

## PlannerAgent

**Responsibility:** Decompose the user query into an ordered execution plan.

| | Fields |
|---|---|
| Reads | `user_query` |
| Writes | `plan`, `requires_graph`, `requires_retrieval` |

**Rules:**
- Must not call any retrieval or graph service
- Output must be a structured list of steps
- Must flag whether graph and/or retrieval are needed

---

## RetrieverAgent

**Responsibility:** Fetch the most relevant code chunks from the vector store.

| | Fields |
|---|---|
| Reads | `user_query`, `requires_retrieval` |
| Writes | `retrieved_chunks` |

**Rules:**
- Must skip execution if `requires_retrieval` is False
- Must use `BaseRetriever` interface (never direct ChromaDB calls)
- Returns ranked `RetrievalResult` list

---

## GraphExplorerAgent

**Responsibility:** Traverse the dependency graph to gather structural context.

| | Fields |
|---|---|
| Reads | `user_query`, `requires_graph`, `retrieved_chunks` |
| Writes | `graph_context` |

**Rules:**
- Must skip execution if `requires_graph` is False
- Must use `BaseGraphStore` interface (never direct NetworkX/Neo4j calls)
- Returns relevant `CodeNode` list

---

## AnalyzerAgent

**Responsibility:** Perform structural reasoning — impact analysis, architecture explanation.

| | Fields |
|---|---|
| Reads | `user_query`, `retrieved_chunks`, `graph_context` |
| Writes | `analysis_notes` |

**Rules:**
- Must not call retrieval or graph services directly
- Works only with already-gathered context
- Output is a structured analysis string passed to the synthesizer

---

## SynthesizerAgent

**Responsibility:** Produce the final, user-facing answer.

| | Fields |
|---|---|
| Reads | `user_query`, `retrieved_chunks`, `graph_context`, `analysis_notes` |
| Writes | `final_answer` |

**Rules:**
- Must be the last agent in every workflow
- Must ground its answer in provided context (no hallucination)
- Must use the prompt from `config/prompts/synthesizer.md`

---

## Rules for all agents

- Must inherit from `BaseAgent`
- Must be testable independently (no hidden dependencies)
- Must use structured logging (`logger.info(...)`, never `print()`)
- Must raise `AgentError` on failure (never bare `Exception`)
- Must be injected with dependencies via `__init__` (never self-instantiate)
