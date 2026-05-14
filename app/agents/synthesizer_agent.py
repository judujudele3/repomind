"""SynthesizerAgent — produces the final user-facing answer."""
import structlog

from app.core.base_agent import BaseAgent
from app.core.base_llm import BaseLLM
from app.domain.exceptions import AgentError
from app.domain.state import AgentState

logger = structlog.get_logger(__name__)


class SynthesizerAgent(BaseAgent):
    """Produces the final grounded answer for the user.

    Reads:  user_query, retrieved_chunks, graph_context, analysis_notes
    Writes: final_answer

    Must always be the last agent in a workflow.
    Must ground its answer in provided context.
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    @property
    def name(self) -> str:
        return "SynthesizerAgent"

    async def run(self, state: AgentState) -> AgentState:
        query = state.get("user_query", "")
        if not query:
            raise AgentError("SynthesizerAgent received an empty user_query.")

        chunks = state.get("retrieved_chunks", [])
        graph_context = state.get("graph_context", [])
        analysis_notes = state.get("analysis_notes", "")

        logger.info(
            "SynthesizerAgent started",
            query=query,
            chunks=len(chunks),
            graph_nodes=len(graph_context),
        )

        # TODO: build synthesizer prompt from config/prompts/synthesizer.md
        # and call self._llm.chat(messages)
        final_answer = (
            f"Synthesis pending implementation. "
            f"Query: {query!r} | "
            f"Chunks: {len(chunks)} | "
            f"Notes: {analysis_notes}"
        )

        logger.info("SynthesizerAgent done")
        return {**state, "final_answer": final_answer}
