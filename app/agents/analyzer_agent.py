"""AnalyzerAgent — performs structural and impact analysis."""
import structlog

from app.core.base_agent import BaseAgent
from app.core.base_llm import BaseLLM
from app.domain.exceptions import AgentError
from app.domain.state import AgentState

logger = structlog.get_logger(__name__)


class AnalyzerAgent(BaseAgent):
    """Synthesizes retrieved chunks and graph context into analysis notes.

    Reads:  user_query, retrieved_chunks, graph_context
    Writes: analysis_notes
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    @property
    def name(self) -> str:
        return "AnalyzerAgent"

    async def run(self, state: AgentState) -> AgentState:
        query = state.get("user_query", "")
        chunks = state.get("retrieved_chunks", [])
        graph_context = state.get("graph_context", [])

        if not query:
            raise AgentError("AnalyzerAgent received an empty user_query.")

        logger.info(
            "AnalyzerAgent started",
            query=query,
            chunks=len(chunks),
            graph_nodes=len(graph_context),
        )

        # TODO: build analyzer prompt from config/prompts/analyzer.md
        # and call self._llm.chat(messages)
        analysis_notes = (
            f"Analysis pending implementation. "
            f"Context: {len(chunks)} chunks, {len(graph_context)} graph nodes."
        )

        logger.info("AnalyzerAgent done")
        return {**state, "analysis_notes": analysis_notes}
