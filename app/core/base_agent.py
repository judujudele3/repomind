"""Abstract base interface for all RepoMind agents."""
from abc import ABC, abstractmethod

from app.domain.state import AgentState


class BaseAgent(ABC):
    """Base interface for all agents in the RepoMind system.

    Each agent must have:
    - A single, well-defined responsibility
    - A clear input (AgentState)
    - A clear output (updated AgentState)
    - An independent, testable run() method

    FORBIDDEN: god-object agents doing retrieval +
    analysis + memory + generation all at once.
    """

    @abstractmethod
    async def run(self, state: AgentState) -> AgentState:
        """Execute the agent's responsibility and return updated state."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the agent."""
        ...
