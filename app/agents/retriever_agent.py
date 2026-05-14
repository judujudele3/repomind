"""RetrieverAgent — fetches relevant code chunks from the vector store."""
import structlog

from app.core.base_agent import BaseAgent
from app.core.base_retriever import BaseRetriever
from app.domain.exceptions import AgentError
from app.domain.state import AgentState

logger = structlog.get_logger(__name__)


class RetrieverAgent(BaseAgent):
    """Fetches relevant code chunks using vector retrieval.

    Reads:  user_query, requires_retrieval
    Writes: retrieved_chunks
    """

    def __init__(self, retriever: BaseRetriever, top_k: int = 5) -> None:
        self._retriever = retriever
        self._top_k = top_k

    @property
    def name(self) -> str:
        return "RetrieverAgent"

    async def run(self, state: AgentState) -> AgentState:
        if not state.get("requires_retrieval", True):
            logger.info("RetrieverAgent skipped (requires_retrieval=False)")
            return {**state, "retrieved_chunks": []}

        query = state.get("user_query", "")
        if not query:
            raise AgentError("RetrieverAgent received an empty user_query.")

        logger.info("RetrieverAgent started", query=query, top_k=self._top_k)

        results = await self._retriever.retrieve(query=query, top_k=self._top_k)

        logger.info("RetrieverAgent done", chunks_retrieved=len(results))
        return {**state, "retrieved_chunks": results}
