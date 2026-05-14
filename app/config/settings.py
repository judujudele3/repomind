"""Application configuration loaded from environment variables.

Never hardcode values. All configuration passes through this module.
"""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """RepoMind application settings."""

    # LLM
    llm_provider: str = Field(default="groq", alias="LLM_PROVIDER")

    # Groq (default — free, fast, no GPU needed)
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")

    # OpenAI
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", alias="OPENAI_MODEL")

    # Ollama (local)
    ollama_model: str = Field(default="llama3", alias="OLLAMA_MODEL")
    ollama_base_url: str = Field(
        default="http://ollama:11434", alias="OLLAMA_BASE_URL"
    )

    # Vector DB
    vector_db: str = Field(default="chroma", alias="VECTOR_DB")
    chroma_host: str = Field(default="chromadb", alias="CHROMA_HOST")
    chroma_port: int = Field(default=8001, alias="CHROMA_PORT")

    # Graph
    graph_backend: str = Field(default="networkx", alias="GRAPH_BACKEND")
    neo4j_uri: str = Field(default="bolt://neo4j:7687", alias="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", alias="NEO4J_USER")
    neo4j_password: str | None = Field(default=None, alias="NEO4J_PASSWORD")

    # App
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    app_env: str = Field(default="development", alias="APP_ENV")

    class Config:
        env_file = ".env"
        populate_by_name = True


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
