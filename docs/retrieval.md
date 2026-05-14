# Retrieval — RepoMind

## Overview

Retrieval is **fully decoupled from agents**. The `retrieval/` layer is independently configurable and extensible.

---

## Current strategy — Vector retrieval

Uses ChromaDB with cosine similarity.

**Flow:**
1. User query → embedding model → query vector
2. Query vector → ChromaDB → top-K chunks
3. Chunks → `RetrievalResult` list (with score + source)

---

## Planned strategies

| Strategy | Description | Status |
|---|---|---|
| Vector | Semantic similarity via embeddings | ✅ v1 |
| Hybrid | Vector + keyword (BM25) fusion | 🔧 v2 |
| Graph-aware | Vector results re-ranked using graph proximity | 🔧 v2 |
| Reranking | Cross-encoder reranking of top candidates | 🔧 v2 |

---

## `RetrievalResult` model

```python
class RetrievalResult(BaseModel):
    chunk: CodeChunk      # The retrieved code chunk
    score: float          # Relevance score (0.0 → 1.0, higher = better)
    source: str           # "vector" | "graph" | "hybrid"
```

---

## Configuration

All retrieval is done through `BaseRetriever`. Switch implementations via dependency injection — no code changes in agents.

```python
# In use case / workflow
retriever: BaseRetriever = ChromaVectorStore(host=..., port=...)
```

---

## Rules

- Retrieval logic must never contain agent logic
- Agents must never call ChromaDB directly — always via `BaseRetriever`
- `top_k` is configurable per call (default: 5)
- Scores are normalized to [0.0, 1.0]
