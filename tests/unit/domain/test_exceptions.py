"""Unit tests for custom exceptions."""
import pytest

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


class TestExceptionHierarchy:
    def test_all_inherit_from_repomind_error(self):
        exceptions = [
            ParsingError,
            EmbeddingError,
            RetrievalError,
            GraphTraversalError,
            IngestionError,
            AgentError,
            ConfigurationError,
            ProviderError,
        ]
        for exc_class in exceptions:
            assert issubclass(exc_class, RepoMindError), (
                f"{exc_class.__name__} must inherit from RepoMindError"
            )

    def test_repomind_error_is_exception(self):
        assert issubclass(RepoMindError, Exception)

    def test_raise_retrieval_error(self):
        with pytest.raises(RetrievalError, match="ChromaDB unavailable"):
            raise RetrievalError("ChromaDB unavailable")

    def test_raise_agent_error(self):
        with pytest.raises(AgentError):
            raise AgentError("empty query")

    def test_catch_as_base(self):
        with pytest.raises(RepoMindError):
            raise GraphTraversalError("node not found")
