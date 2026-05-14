"""PlannerAgent — decomposes user query into an execution plan."""
import structlog

from app.core.base_agent import BaseAgent
from app.core.base_llm import BaseLLM
from app.domain.exceptions import AgentError
from app.domain.state import AgentState

logger = structlog.get_logger(__name__)


class PlannerAgent(BaseAgent):
    """Analyses the user query and produces a structured execution plan.

    Reads:  user_query
    Writes: plan, requires_graph, requires_retrieval
    """

    def __init__(self, llm: BaseLLM) -> None:
        self._llm = llm

    @property
    def name(self) -> str:
        return "PlannerAgent"

    async def run(self, state: AgentState) -> AgentState:
        query = state.get("user_query", "")
        if not query:
            raise AgentError("PlannerAgent received an empty user_query.")

        logger.info("PlannerAgent started", query=query)

        # TODO: call self._llm with planner prompt
        # For now: default plan (retrieval + graph)
        plan = [
            "retrieve relevant code chunks",
            "explore dependency graph",
            "analyze structural context",
            "synthesize final answer",
        ]

        updated: AgentState = {
            **state,
            "plan": plan,
            "requires_retrieval": True,
            "requires_graph": True,
            "iteration": state.get("iteration", 0) + 1,
        }

        logger.info("PlannerAgent done", plan=plan)
        return updated
