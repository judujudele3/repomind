"""Neo4j-based graph store (persistent, production-ready)."""
import logging

from app.core.base_graph_store import BaseGraphStore
from app.domain.exceptions import GraphTraversalError
from app.domain.models import CodeNode, DependencyEdge

logger = logging.getLogger(__name__)


class Neo4jGraphStore(BaseGraphStore):
    """Persistent dependency graph using Neo4j.

    Requires NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD env variables.

    Note: Full implementation pending. Switch via GRAPH_BACKEND=neo4j.
    """

    def __init__(self, uri: str, user: str, password: str) -> None:
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        logger.info("Neo4j graph store initialized", uri=uri)

    async def add_node(self, node: CodeNode) -> None:
        raise NotImplementedError("Neo4j implementation pending")

    async def add_edge(self, edge: DependencyEdge) -> None:
        raise NotImplementedError("Neo4j implementation pending")

    async def get_neighbors(self, node_id: str, depth: int = 1) -> list[CodeNode]:
        raise NotImplementedError("Neo4j implementation pending")

    async def get_dependencies(self, node_id: str) -> list[CodeNode]:
        raise NotImplementedError("Neo4j implementation pending")

    async def get_dependents(self, node_id: str) -> list[CodeNode]:
        raise NotImplementedError("Neo4j implementation pending")

    async def clear(self) -> None:
        raise NotImplementedError("Neo4j implementation pending")
