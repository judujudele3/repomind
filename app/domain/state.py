"""Centralized agent state for LangGraph workflows.

All workflows share a single typed state. No agent
may modify the state arbitrarily outside its contract.
"""
from typing import TypedDict

from app.domain.models import CodeNode, RetrievalResult


class AgentState(TypedDict, total=False):
    """Shared state passed between all agents in a workflow.

    Fields are optional (total=False) to allow partial updates,
    but each agent must document which fields it reads and writes.
    """

    # --- Input ---
    user_query: str
    """The raw user question or instruction."""

    repository_path: str
    """Absolute path to the ingested repository."""

    # --- Planner output ---
    plan: list[str]
    """Ordered list of steps produced by PlannerAgent."""

    requires_graph: bool
    """Whether the query needs graph exploration."""

    requires_retrieval: bool
    """Whether the query needs vector retrieval."""

    # --- Retriever output ---
    retrieved_chunks: list[RetrievalResult]
    """Chunks retrieved from the vector store."""

    # --- Graph explorer output ---
    graph_context: list[CodeNode]
    """Nodes retrieved from the dependency graph."""

    # --- Analyzer output ---
    analysis_notes: str
    """Structural analysis or impact notes."""

    # --- Synthesizer output ---
    final_answer: str
    """The final response to the user."""

    # --- Metadata ---
    error: str | None
    """Error message if any agent failed."""

    iteration: int
    """Current workflow iteration (for loop detection)."""
