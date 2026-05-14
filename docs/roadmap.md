# Roadmap — RepoMind

## v1 — MVP (current)

### Infrastructure ✅
- [x] Project structure (Clean Architecture)
- [x] Core abstractions (BaseLLM, BaseAgent, BaseRetriever, BaseGraphStore, BaseEmbeddingModel)
- [x] Domain models (CodeChunk, CodeNode, DependencyEdge, RetrievalResult, AgentState)
- [x] Custom exceptions
- [x] OpenAI + Ollama providers (switchable)
- [x] ChromaDB vector store
- [x] NetworkX + Neo4j graph stores (switchable)
- [x] Docker environment (app + ChromaDB + Ollama profile)
- [x] Structured logging (structlog)
- [x] Configuration (Pydantic Settings)

### To implement 🔧
- [ ] Repository ingestion pipeline (AST parsing → chunks → embeddings → graph)
- [ ] Tree-sitter Python parser
- [ ] Dependency graph builder
- [ ] Agent implementations (Planner, Retriever, GraphExplorer, Analyzer, Synthesizer)
- [ ] LangGraph workflow wiring
- [ ] Use cases (AnalyzeRepository, AnswerQuery, GenerateImpactReport)
- [ ] FastAPI routes (ingest, query, impact)
- [ ] CLI interface
- [ ] Test suite (unit + integration)

### MVP success criteria
The MVP is complete when a developer can:
1. Point RepoMind at a Python repo
2. Ask "What does module X depend on?"
3. Ask "What breaks if I change function Y?"
4. Get accurate, context-grounded answers

---

## v2 — Future work (out of scope for v1)

These features must not influence v1 architecture decisions.

| Feature | Description |
|---|---|
| Multi-language parsing | TypeScript, Go, Rust support |
| MCP integration | Model Context Protocol server |
| GitHub integration | PR review agents, diff analysis |
| IDE plugin | VSCode / JetBrains extension |
| Multi-repo memory | Cross-repository understanding |
| Semantic diffing | Understand what changed between commits |
| Graph RAG | Graph-aware retrieval strategies |
| Temporal memory | Track how the codebase evolves over time |
| PR generation | Auto-generate pull requests from analysis |
| Multi-user system | Auth, namespacing, team features |
