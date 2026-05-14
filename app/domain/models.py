"""Domain models for RepoMind.

This module contains ONLY business entities and typed models.
NO infrastructure imports allowed here (FastAPI, Chroma, LangGraph, OpenAI).
"""
from enum import Enum

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class NodeType(str, Enum):
    """Type of a code node in the dependency graph."""

    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    METHOD = "method"
    IMPORT = "import"


class EdgeType(str, Enum):
    """Type of relationship between two code nodes."""

    IMPORTS = "imports"
    INHERITS = "inherits"
    CALLS = "calls"
    DEFINES = "defines"
    USES = "uses"


class ChunkType(str, Enum):
    """Type of a parsed code chunk."""

    FUNCTION = "function"
    CLASS = "class"
    MODULE = "module"
    DOCSTRING = "docstring"
    BLOCK = "block"


# ---------------------------------------------------------------------------
# Core domain entities
# ---------------------------------------------------------------------------


class CodeChunk(BaseModel):
    """A semantically meaningful piece of source code."""

    id: str = Field(description="Unique identifier for this chunk.")
    file_path: str = Field(description="Relative path to the source file.")
    content: str = Field(description="Raw source code content of the chunk.")
    chunk_type: ChunkType = Field(description="Semantic type of the chunk.")
    start_line: int = Field(description="Starting line number in the file.")
    end_line: int = Field(description="Ending line number in the file.")
    name: str | None = Field(
        default=None,
        description="Name of the function, class, or module if applicable.",
    )
    docstring: str | None = Field(
        default=None,
        description="Extracted docstring if present.",
    )
    embedding: list[float] | None = Field(
        default=None,
        description="Vector embedding for this chunk.",
        exclude=True,
    )

    class Config:
        frozen = True


class CodeNode(BaseModel):
    """A node in the code dependency graph."""

    id: str = Field(description="Unique identifier (e.g., 'module.ClassName').")
    name: str = Field(description="Simple name of the code element.")
    node_type: NodeType = Field(description="Type of the code element.")
    file_path: str = Field(description="Relative path to the source file.")
    line: int | None = Field(
        default=None,
        description="Line number where the element is defined.",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Additional metadata (e.g., decorators, return type).",
    )

    class Config:
        frozen = True


class DependencyEdge(BaseModel):
    """A directed edge in the code dependency graph."""

    source_id: str = Field(description="ID of the source node.")
    target_id: str = Field(description="ID of the target node.")
    edge_type: EdgeType = Field(description="Type of the relationship.")
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Additional metadata about the relationship.",
    )

    class Config:
        frozen = True


class RetrievalResult(BaseModel):
    """The result of a retrieval operation."""

    chunk: CodeChunk = Field(description="The retrieved code chunk.")
    score: float = Field(description="Relevance score (higher is better).")
    source: str = Field(
        default="vector",
        description="Origin of the result (e.g., 'vector', 'graph', 'hybrid').",
    )
