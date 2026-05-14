"""NetworkX-based graph store (local, in-memory)."""
import logging

import networkx as nx

from app.core.base_graph_store import BaseGraphStore
from app.domain.exceptions import GraphTraversalError
from app.domain.models import CodeNode, DependencyEdge

logger = logging.getLogger(__name__)


class NetworkXGraphStore(BaseGraphStore):
    """In-memory dependency graph using NetworkX.

    Suitable for local development and v1 MVP.
    For persistence, use Neo4jGraphStore.
    """

    def __init__(self) -> None:
        self._graph: nx.DiGraph = nx.DiGraph()

    async def add_node(self, node: CodeNode) -> None:
        logger.info("Adding graph node", node_id=node.id, node_type=node.node_type)
        self._graph.add_node(node.id, **node.model_dump())

    async def add_edge(self, edge: DependencyEdge) -> None:
        logger.info(
            "Adding graph edge",
            source=edge.source_id,
            target=edge.target_id,
            edge_type=edge.edge_type,
        )
        self._graph.add_edge(
            edge.source_id,
            edge.target_id,
            edge_type=edge.edge_type,
            **edge.metadata,
        )

    async def get_neighbors(self, node_id: str, depth: int = 1) -> list[CodeNode]:
        try:
            neighbors = nx.ego_graph(self._graph, node_id, radius=depth).nodes
            return [
                CodeNode(**self._graph.nodes[n])
                for n in neighbors
                if n != node_id
            ]
        except Exception as exc:
            raise GraphTraversalError(
                f"Failed to get neighbors of '{node_id}': {exc}"
            ) from exc

    async def get_dependencies(self, node_id: str) -> list[CodeNode]:
        try:
            return [
                CodeNode(**self._graph.nodes[n])
                for n in self._graph.successors(node_id)
            ]
        except Exception as exc:
            raise GraphTraversalError(
                f"Failed to get dependencies of '{node_id}': {exc}"
            ) from exc

    async def get_dependents(self, node_id: str) -> list[CodeNode]:
        try:
            return [
                CodeNode(**self._graph.nodes[n])
                for n in self._graph.predecessors(node_id)
            ]
        except Exception as exc:
            raise GraphTraversalError(
                f"Failed to get dependents of '{node_id}': {exc}"
            ) from exc

    async def clear(self) -> None:
        self._graph.clear()
        logger.info("Graph store cleared")
