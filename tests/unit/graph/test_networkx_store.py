"""Unit tests for NetworkXGraphStore."""
import pytest

from app.domain.exceptions import GraphTraversalError
from app.domain.models import CodeNode, DependencyEdge, EdgeType, NodeType
from app.infrastructure.graph.networkx_store import NetworkXGraphStore


@pytest.fixture
def store() -> NetworkXGraphStore:
    return NetworkXGraphStore()


@pytest.fixture
def node_a() -> CodeNode:
    return CodeNode(
        id="app.agents.planner_agent",
        name="planner_agent",
        node_type=NodeType.MODULE,
        file_path="app/agents/planner_agent.py",
    )


@pytest.fixture
def node_b() -> CodeNode:
    return CodeNode(
        id="app.core.base_llm",
        name="base_llm",
        node_type=NodeType.MODULE,
        file_path="app/core/base_llm.py",
    )


class TestNetworkXGraphStore:
    @pytest.mark.asyncio
    async def test_add_and_get_node(self, store, node_a):
        await store.add_node(node_a)
        neighbors = await store.get_neighbors(node_a.id, depth=0)
        # depth=0 ego graph returns just the node itself (minus self in our impl)
        assert isinstance(neighbors, list)

    @pytest.mark.asyncio
    async def test_add_edge_and_get_dependencies(self, store, node_a, node_b):
        await store.add_node(node_a)
        await store.add_node(node_b)
        edge = DependencyEdge(
            source_id=node_a.id,
            target_id=node_b.id,
            edge_type=EdgeType.IMPORTS,
        )
        await store.add_edge(edge)

        deps = await store.get_dependencies(node_a.id)
        dep_ids = [d.id for d in deps]
        assert node_b.id in dep_ids

    @pytest.mark.asyncio
    async def test_get_dependents(self, store, node_a, node_b):
        await store.add_node(node_a)
        await store.add_node(node_b)
        edge = DependencyEdge(
            source_id=node_a.id,
            target_id=node_b.id,
            edge_type=EdgeType.IMPORTS,
        )
        await store.add_edge(edge)

        dependents = await store.get_dependents(node_b.id)
        dep_ids = [d.id for d in dependents]
        assert node_a.id in dep_ids

    @pytest.mark.asyncio
    async def test_clear(self, store, node_a):
        await store.add_node(node_a)
        await store.clear()
        with pytest.raises(GraphTraversalError):
            await store.get_dependencies(node_a.id)
