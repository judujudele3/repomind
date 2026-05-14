"""Shared pytest fixtures for RepoMind test suite."""
import pytest

from app.domain.models import ChunkType, CodeChunk, CodeNode, NodeType


@pytest.fixture
def sample_chunk() -> CodeChunk:
    return CodeChunk(
        id="test_chunk_001",
        file_path="app/agents/planner_agent.py",
        content="class PlannerAgent(BaseAgent):\n    ...",
        chunk_type=ChunkType.CLASS,
        start_line=1,
        end_line=20,
        name="PlannerAgent",
        docstring="Decomposes user query into an execution plan.",
    )


@pytest.fixture
def sample_node() -> CodeNode:
    return CodeNode(
        id="app.agents.planner_agent.PlannerAgent",
        name="PlannerAgent",
        node_type=NodeType.CLASS,
        file_path="app/agents/planner_agent.py",
        line=10,
    )
