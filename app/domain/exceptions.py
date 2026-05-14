"""Custom exceptions for RepoMind.

Always raise domain-specific exceptions instead of bare Exception.
This enables precise error handling and better observability.
"""


class RepoMindError(Exception):
    """Base exception for all RepoMind errors."""


class ParsingError(RepoMindError):
    """Raised when source code parsing fails."""


class EmbeddingError(RepoMindError):
    """Raised when embedding generation fails."""


class RetrievalError(RepoMindError):
    """Raised when vector retrieval fails."""


class GraphTraversalError(RepoMindError):
    """Raised when graph traversal fails."""


class IngestionError(RepoMindError):
    """Raised when repository ingestion fails."""


class AgentError(RepoMindError):
    """Raised when an agent fails to execute."""


class ConfigurationError(RepoMindError):
    """Raised when configuration is invalid or missing."""


class ProviderError(RepoMindError):
    """Raised when an external provider (LLM, DB) fails."""
