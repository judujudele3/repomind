"""Basic ingestion parser for RepoMind.

This module parses a single Python source file into a
module-level CodeChunk using the standard `ast` module.
"""
import ast
from pathlib import Path

from app.domain.models import ChunkType, CodeChunk


def parse_file(file_path: str) -> list[CodeChunk]:
    """Parse a Python file into a list containing one module-level chunk.

    This is a first, minimal version: it does NOT yet split the file
    into functions/classes. It reads the whole file and wraps it in
    a single CodeChunk of type MODULE.

    Args:
        file_path: Path to the .py file to parse.

    Returns:
        A list containing a single CodeChunk representing the module.

    Raises:
        SyntaxError: If the file contains invalid Python syntax.
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    # Validate that the file is syntactically valid Python.
    # We parse it now even though we don't use the tree yet,
    # so that broken files fail fast during ingestion.
    tree = ast.parse(content, filename=str(path))

    docstring = ast.get_docstring(tree)
    total_lines = content.count("\n") + 1

    chunk = CodeChunk(
        id=str(path),
        file_path=str(path),
        content=content,
        chunk_type=ChunkType.MODULE,
        start_line=1,
        end_line=total_lines,
        name=path.stem,
        docstring=docstring,
    )

    return [chunk]