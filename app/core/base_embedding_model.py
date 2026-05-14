"""Abstract base interface for embedding models."""
from abc import ABC, abstractmethod


class BaseEmbeddingModel(ABC):
    """Base interface for all embedding model implementations.

    Allows swapping between OpenAI, local, or other
    embedding providers without changing business logic.
    """

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single text."""
        ...

    @abstractmethod
    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for a batch of texts."""
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return the dimensionality of the embedding vectors."""
        ...
