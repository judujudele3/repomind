"""Abstract base interface for graph store backends."""
from abc import ABC, abstractmethod

from app.domain.models import CodeNode, DependencyEdge


class BaseGraphStore(ABC):
    """Base interface for graph storage backends.

    Implementations include NetworkX (local) and Neo4j (persistent).
    """

    @abstractmethod
    async def add_node(self, node: CodeNode) -> None:
        """Add a code node to the graph."""
        ...

    @abstractmethod
    async def add_edge(self, edge: DependencyEdge) -> None:
        """Add a dependency edge between two nodes."""
        ...

    @abstractmethod
    async def get_neighbors(
        self,
        node_id: str,
        depth: int = 1,
    ) -> list[CodeNode]:
        """Return neighboring nodes up to a given depth."""
        ...

    @abstractmethod
    async def get_dependencies(self, node_id: str) -> list[CodeNode]:
        """Return all direct dependencies of a node."""
        ...

    @abstractmethod
    async def get_dependents(self, node_id: str) -> list[CodeNode]:
        """Return all nodes that depend on the given node."""
        ...

    @abstractmethod
    async def clear(self) -> None:
        """Clear the entire graph."""
        ...
