"""Abstract base interface for retrieval components."""
from abc import ABC, abstractmethod

from app.domain.models import CodeChunk, RetrievalResult


class BaseRetriever(ABC):
    """Base interface for all retrieval strategies.

    Implementations can include vector retrieval,
    hybrid retrieval, graph-aware retrieval, etc.
    """

    @abstractmethod
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        **kwargs,
    ) -> list[RetrievalResult]:
        """Retrieve the most relevant chunks for a query."""
        ...

    @abstractmethod
    async def index(self, chunks: list[CodeChunk]) -> None:
        """Index a list of code chunks for future retrieval."""
        ...
