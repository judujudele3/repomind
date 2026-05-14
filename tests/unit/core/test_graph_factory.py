"""Unit tests for graph store factory."""
import pytest

from app.domain.exceptions import ConfigurationError
from app.infrastructure.graph.factory import create_graph_store
from app.infrastructure.graph.networkx_store import NetworkXGraphStore


class TestGraphFactory:
    def test_creates_networkx_store(self, monkeypatch):
        monkeypatch.setenv("GRAPH_BACKEND", "networkx")
        store = create_graph_store()
        assert isinstance(store, NetworkXGraphStore)

    def test_default_is_networkx(self, monkeypatch):
        monkeypatch.delenv("GRAPH_BACKEND", raising=False)
        store = create_graph_store()
        assert isinstance(store, NetworkXGraphStore)

    def test_raises_on_unknown_backend(self, monkeypatch):
        monkeypatch.setenv("GRAPH_BACKEND", "redis")
        with pytest.raises(ConfigurationError, match="Unsupported GRAPH_BACKEND"):
            create_graph_store()

    def test_raises_neo4j_without_password(self, monkeypatch):
        monkeypatch.setenv("GRAPH_BACKEND", "neo4j")
        monkeypatch.delenv("NEO4J_PASSWORD", raising=False)
        with pytest.raises(ConfigurationError, match="NEO4J_PASSWORD"):
            create_graph_store()
