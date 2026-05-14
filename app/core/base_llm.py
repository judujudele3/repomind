"""Abstract base interface for LLM providers."""
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """Base interface for all LLM providers.

    All concrete implementations (OpenAI, Ollama, etc.)
    must inherit from this class.
    """

    @abstractmethod
    async def complete(self, prompt: str, **kwargs) -> str:
        """Generate a completion for the given prompt."""
        ...

    @abstractmethod
    async def chat(self, messages: list[dict], **kwargs) -> str:
        """Generate a response for a conversation."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the name of the underlying model."""
        ...
