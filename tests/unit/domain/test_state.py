"""Unit tests for AgentState."""
from app.domain.state import AgentState


class TestAgentState:
    def test_minimal_state(self):
        state: AgentState = {"user_query": "What does UserService do?"}
        assert state["user_query"] == "What does UserService do?"

    def test_full_state(self):
        state: AgentState = {
            "user_query": "What breaks if I delete auth.py?",
            "repository_path": "/repos/myproject",
            "plan": ["retrieve chunks", "explore graph", "analyze", "synthesize"],
            "requires_graph": True,
            "requires_retrieval": True,
            "retrieved_chunks": [],
            "graph_context": [],
            "analysis_notes": "auth.py is imported by 5 modules.",
            "final_answer": "Deleting auth.py will break: ...",
            "error": None,
            "iteration": 1,
        }
        assert state["requires_graph"] is True
        assert len(state["plan"]) == 4
        assert state["iteration"] == 1

    def test_state_is_partial(self):
        # AgentState uses total=False — all fields are optional
        state: AgentState = {}
        assert state.get("final_answer") is None
        assert state.get("error") is None
