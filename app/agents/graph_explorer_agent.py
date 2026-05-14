"""GraphExplorerAgent — traverses the dependency graph for structural context."""
import structlog

from app.core.base_agent import BaseAgent
from app.core.base_graph_store import BaseGraphStore
from app.domain.exceptions import AgentError
from app.domain.state import AgentState

logger = structlog.get_logger(__name__)


class GraphExplorerAgent(BaseAgent):
    """Traverses the dependency graph to gather structural context.

    Reads:  user_query, requires_graph, retrieved_chunks
    Writes: graph_context
    """

    def __init__(self, graph_store: BaseGraphStore, depth: int = 2) -> None:
        self._graph_store = graph_store
        self._depth = depth

    @property
    def name(self) -> str:
        return "GraphExplorerAgent"

    async def run(self, state: AgentState) -> AgentState:
        if not state.get("requires_graph", True):
            logger.info("GraphExplorerAgent skipped (requires_graph=False)")
            return {**state, "graph_context": []}

        chunks = state.get("retrieved_chunks", [])
        if not chunks:
            logger.info("GraphExplorerAgent: no chunks to explore from")
            return {**state, "graph_context": []}

        logger.info(
            "GraphExplorerAgent started",
            chunk_count=len(chunks),
            depth=self._depth,
        )

        # TODO: extract node IDs from chunks and traverse graph
        # node_ids = [derive_node_id(c.chunk) for c in chunks]
        # graph_context = [await self._graph_store.get_neighbors(n, self._depth) for n in node_ids]

        logger.info("GraphExplorerAgent done", graph_nodes=0)
        return {**state, "graph_context": []}
