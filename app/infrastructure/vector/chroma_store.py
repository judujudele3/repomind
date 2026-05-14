"""ChromaDB vector store implementation."""
import logging

import chromadb

from app.core.base_retriever import BaseRetriever
from app.domain.exceptions import RetrievalError
from app.domain.models import ChunkType, CodeChunk, RetrievalResult

logger = logging.getLogger(__name__)

COLLECTION_NAME = "repomind_chunks"


class ChromaVectorStore(BaseRetriever):
    """Vector retrieval backend using ChromaDB."""

    def __init__(self, host: str = "chromadb", port: int = 8001) -> None:
        self._client = chromadb.HttpClient(host=host, port=port)
        self._collection = self._client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info("ChromaDB connected", host=host, port=port)

    async def index(self, chunks: list[CodeChunk]) -> None:
        try:
            logger.info("Indexing chunks", count=len(chunks))
            ids = [c.id for c in chunks]
            documents = [c.content for c in chunks]
            metadatas = [
                {
                    "file_path": c.file_path,
                    "chunk_type": c.chunk_type.value,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "name": c.name or "",
                }
                for c in chunks
            ]
            embeddings = [c.embedding for c in chunks if c.embedding is not None]

            self._collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings if embeddings else None,
            )
        except Exception as exc:
            raise RetrievalError(f"ChromaDB indexing failed: {exc}") from exc

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        **kwargs,
    ) -> list[RetrievalResult]:
        try:
            logger.info("Vector retrieval started", query=query, top_k=top_k)
            results = self._collection.query(
                query_texts=[query],
                n_results=top_k,
            )
            chunks = []
            for i, doc_id in enumerate(results["ids"][0]):
                meta = results["metadatas"][0][i]
                distance = results["distances"][0][i]
                chunk = CodeChunk(
                    id=doc_id,
                    file_path=meta["file_path"],
                    content=results["documents"][0][i],
                    chunk_type=ChunkType(meta["chunk_type"]),
                    start_line=meta["start_line"],
                    end_line=meta["end_line"],
                    name=meta.get("name") or None,
                )
                chunks.append(
                    RetrievalResult(
                        chunk=chunk,
                        score=1.0 - distance,
                        source="vector",
                    )
                )
            return chunks
        except Exception as exc:
            raise RetrievalError(f"ChromaDB retrieval failed: {exc}") from exc
