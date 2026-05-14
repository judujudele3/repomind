# Graph Model — RepoMind

## Overview

The dependency graph represents the structural relationships between all code elements in a repository.
It is a **directed graph** where nodes are code elements and edges are relationships.

---

## Nodes — `CodeNode`

| Field | Type | Description |
|---|---|---|
| `id` | `str` | Unique identifier, e.g. `mymodule.MyClass.my_method` |
| `name` | `str` | Simple name, e.g. `my_method` |
| `node_type` | `NodeType` | `module`, `class`, `function`, `method`, `import` |
| `file_path` | `str` | Relative path to source file |
| `line` | `int` | Line number of definition |
| `metadata` | `dict` | Extra info (decorators, return type, etc.) |

---

## Edges — `DependencyEdge`

| Field | Type | Description |
|---|---|---|
| `source_id` | `str` | ID of the source node |
| `target_id` | `str` | ID of the target node |
| `edge_type` | `EdgeType` | `imports`, `inherits`, `calls`, `defines`, `uses` |
| `metadata` | `dict` | Extra info (line of call, etc.) |

---

## Edge types

| Type | Meaning |
|---|---|
| `imports` | Module A imports module B |
| `inherits` | Class A extends class B |
| `calls` | Function A calls function B |
| `defines` | Module A defines class/function B |
| `uses` | Function A uses class/type B |

---

## Example graph

```
app.ingestion.parser (module)
    --defines--> app.ingestion.parser.PythonParser (class)
    --imports--> app.domain.models (module)

app.ingestion.parser.PythonParser (class)
    --defines--> app.ingestion.parser.PythonParser.parse (method)
    --inherits--> app.core.base_parser.BaseParser (class)

app.ingestion.parser.PythonParser.parse (method)
    --calls--> app.domain.models.CodeChunk (class)
```

---

## Traversal operations

| Operation | Description |
|---|---|
| `get_dependencies(node_id)` | What does this node depend on? |
| `get_dependents(node_id)` | What depends on this node? (impact analysis) |
| `get_neighbors(node_id, depth)` | Full neighborhood at depth N |

---

## Backends

| Backend | Use case |
|---|---|
| `NetworkXGraphStore` | Local development, in-memory, fast setup |
| `Neo4jGraphStore` | Production, persistent, Cypher queries |

Switch via `GRAPH_BACKEND=networkx` or `GRAPH_BACKEND=neo4j` in `.env`.
