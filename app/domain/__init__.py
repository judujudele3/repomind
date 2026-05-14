"""Domain layer — business entities, state, and exceptions.

NO infrastructure imports allowed in this package.
"""
from app.domain.exceptions import (
    AgentError,
    ConfigurationError,
    EmbeddingError,
    GraphTraversalError,
    IngestionError,
    ParsingError,
    ProviderError,
    RepoMindError,
    RetrievalError,
)
from app.domain.models import (
    ChunkType,
    CodeChunk,
    CodeNode,
    DependencyEdge,
    EdgeType,
    NodeType,
    RetrievalResult,
)
from app.domain.state import AgentState

__all__ = [
    "CodeChunk", "CodeNode", "DependencyEdge", "RetrievalResult",
    "NodeType", "EdgeType", "ChunkType",
    "AgentState",
    "RepoMindError", "ParsingError", "EmbeddingError", "RetrievalError",
    "GraphTraversalError", "IngestionError", "AgentError",
    "ConfigurationError", "ProviderError",
]
