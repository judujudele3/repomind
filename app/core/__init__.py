"""Core abstractions for RepoMind.

All concrete implementations must depend on these interfaces,
never on each other directly.
"""
from app.core.base_agent import BaseAgent
from app.core.base_embedding_model import BaseEmbeddingModel
from app.core.base_graph_store import BaseGraphStore
from app.core.base_llm import BaseLLM
from app.core.base_retriever import BaseRetriever

__all__ = [
    "BaseLLM",
    "BaseRetriever",
    "BaseGraphStore",
    "BaseAgent",
    "BaseEmbeddingModel",
]
