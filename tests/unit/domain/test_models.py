"""Unit tests for domain models."""
import pytest

from app.domain.models import (
    ChunkType,
    CodeChunk,
    CodeNode,
    DependencyEdge,
    EdgeType,
    NodeType,
    RetrievalResult,
)


class TestCodeChunk:
    def test_create_minimal(self):
        chunk = CodeChunk(
            id="chunk_001",
            file_path="app/core/base_llm.py",
            content="class BaseLLM(ABC): ...",
            chunk_type=ChunkType.CLASS,
            start_line=1,
            end_line=10,
        )
        assert chunk.id == "chunk_001"
        assert chunk.chunk_type == ChunkType.CLASS
        assert chunk.name is None
        assert chunk.embedding is None

    def test_create_with_all_fields(self):
        chunk = CodeChunk(
            id="chunk_002",
            file_path="app/core/base_llm.py",
            content="async def complete(self, prompt: str) -> str: ...",
            chunk_type=ChunkType.FUNCTION,
            start_line=5,
            end_line=8,
            name="complete",
            docstring="Generate a completion.",
        )
        assert chunk.name == "complete"
        assert chunk.docstring == "Generate a completion."

    def test_immutability(self):
        chunk = CodeChunk(
            id="chunk_003",
            file_path="app/domain/models.py",
            content="pass",
            chunk_type=ChunkType.MODULE,
            start_line=1,
            end_line=1,
        )
        with pytest.raises(Exception):
            chunk.id = "modified"  # type: ignore


class TestCodeNode:
    def test_create(self):
        node = CodeNode(
            id="app.core.base_llm.BaseLLM",
            name="BaseLLM",
            node_type=NodeType.CLASS,
            file_path="app/core/base_llm.py",
            line=10,
        )
        assert node.id == "app.core.base_llm.BaseLLM"
        assert node.node_type == NodeType.CLASS

    def test_metadata_defaults_empty(self):
        node = CodeNode(
            id="app.domain.models",
            name="models",
            node_type=NodeType.MODULE,
            file_path="app/domain/models.py",
        )
        assert node.metadata == {}


class TestDependencyEdge:
    def test_create(self):
        edge = DependencyEdge(
            source_id="app.agents.planner_agent",
            target_id="app.core.base_llm",
            edge_type=EdgeType.IMPORTS,
        )
        assert edge.edge_type == EdgeType.IMPORTS
        assert edge.metadata == {}


class TestRetrievalResult:
    def test_create(self):
        chunk = CodeChunk(
            id="chunk_001",
            file_path="app/agents/planner_agent.py",
            content="class PlannerAgent(BaseAgent): ...",
            chunk_type=ChunkType.CLASS,
            start_line=1,
            end_line=20,
        )
        result = RetrievalResult(chunk=chunk, score=0.92, source="vector")
        assert result.score == 0.92
        assert result.source == "vector"

    def test_default_source(self):
        chunk = CodeChunk(
            id="chunk_002",
            file_path="app/domain/models.py",
            content="pass",
            chunk_type=ChunkType.MODULE,
            start_line=1,
            end_line=1,
        )
        result = RetrievalResult(chunk=chunk, score=0.75)
        assert result.source == "vector"
