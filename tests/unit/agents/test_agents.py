"""Unit tests for agents."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.agents.planner_agent import PlannerAgent
from app.agents.retriever_agent import RetrieverAgent
from app.agents.synthesizer_agent import SynthesizerAgent
from app.domain.exceptions import AgentError
from app.domain.state import AgentState


class TestPlannerAgent:
    @pytest.fixture
    def agent(self):
        llm = MagicMock()
        return PlannerAgent(llm=llm)

    def test_name(self, agent):
        assert agent.name == "PlannerAgent"

    @pytest.mark.asyncio
    async def test_run_produces_plan(self, agent):
        state: AgentState = {"user_query": "What does UserService do?"}
        result = await agent.run(state)

        assert "plan" in result
        assert isinstance(result["plan"], list)
        assert len(result["plan"]) > 0
        assert "requires_retrieval" in result
        assert "requires_graph" in result
        assert result["iteration"] == 1

    @pytest.mark.asyncio
    async def test_run_increments_iteration(self, agent):
        state: AgentState = {"user_query": "test", "iteration": 3}
        result = await agent.run(state)
        assert result["iteration"] == 4

    @pytest.mark.asyncio
    async def test_raises_on_empty_query(self, agent):
        with pytest.raises(AgentError):
            await agent.run({"user_query": ""})


class TestRetrieverAgent:
    @pytest.fixture
    def mock_retriever(self):
        retriever = AsyncMock()
        retriever.retrieve = AsyncMock(return_value=[])
        return retriever

    @pytest.fixture
    def agent(self, mock_retriever):
        return RetrieverAgent(retriever=mock_retriever, top_k=3)

    def test_name(self, agent):
        assert agent.name == "RetrieverAgent"

    @pytest.mark.asyncio
    async def test_skips_when_not_required(self, agent, mock_retriever):
        state: AgentState = {
            "user_query": "test",
            "requires_retrieval": False,
        }
        result = await agent.run(state)
        assert result["retrieved_chunks"] == []
        mock_retriever.retrieve.assert_not_called()

    @pytest.mark.asyncio
    async def test_calls_retriever_when_required(self, agent, mock_retriever):
        state: AgentState = {
            "user_query": "What does UserService do?",
            "requires_retrieval": True,
        }
        result = await agent.run(state)
        mock_retriever.retrieve.assert_called_once_with(
            query="What does UserService do?", top_k=3
        )
        assert "retrieved_chunks" in result

    @pytest.mark.asyncio
    async def test_raises_on_empty_query(self, agent):
        with pytest.raises(AgentError):
            await agent.run({"user_query": "", "requires_retrieval": True})


class TestSynthesizerAgent:
    @pytest.fixture
    def agent(self):
        llm = MagicMock()
        return SynthesizerAgent(llm=llm)

    def test_name(self, agent):
        assert agent.name == "SynthesizerAgent"

    @pytest.mark.asyncio
    async def test_writes_final_answer(self, agent):
        state: AgentState = {
            "user_query": "What does UserService do?",
            "retrieved_chunks": [],
            "graph_context": [],
            "analysis_notes": "UserService handles authentication.",
        }
        result = await agent.run(state)
        assert "final_answer" in result
        assert isinstance(result["final_answer"], str)

    @pytest.mark.asyncio
    async def test_raises_on_empty_query(self, agent):
        with pytest.raises(AgentError):
            await agent.run({"user_query": ""})
