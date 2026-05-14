"""Factory to instantiate the correct graph store from config."""
import os

from app.core.base_graph_store import BaseGraphStore
from app.domain.exceptions import ConfigurationError
from app.infrastructure.graph.neo4j_store import Neo4jGraphStore
from app.infrastructure.graph.networkx_store import NetworkXGraphStore


def create_graph_store() -> BaseGraphStore:
    """Instantiate the graph store based on GRAPH_BACKEND env variable.

    Supported values: 'networkx', 'neo4j'
    """
    backend = os.getenv("GRAPH_BACKEND", "networkx").lower()

    if backend == "networkx":
        return NetworkXGraphStore()

    if backend == "neo4j":
        uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD")
        if not password:
            raise ConfigurationError(
                "NEO4J_PASSWORD is required when GRAPH_BACKEND=neo4j"
            )
        return Neo4jGraphStore(uri=uri, user=user, password=password)

    raise ConfigurationError(
        f"Unsupported GRAPH_BACKEND: '{backend}'. Choose 'networkx' or 'neo4j'."
    )
