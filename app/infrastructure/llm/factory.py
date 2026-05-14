"""Factory to instantiate the correct LLM provider from config."""
import os

from app.core.base_llm import BaseLLM
from app.domain.exceptions import ConfigurationError
from app.infrastructure.llm.groq_client import GroqClient
from app.infrastructure.llm.ollama_client import OllamaClient
from app.infrastructure.llm.openai_client import OpenAIClient


def create_llm() -> BaseLLM:
    """Instantiate the LLM provider based on LLM_PROVIDER env variable.

    Supported values: 'openai', 'ollama', 'groq'
    """
    provider = os.getenv("LLM_PROVIDER", "groq").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai"
            )
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
        return OpenAIClient(api_key=api_key, model=model)

    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ConfigurationError(
                "GROQ_API_KEY is required when LLM_PROVIDER=groq. "
                "Get a free key at https://console.groq.com"
            )
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        return GroqClient(api_key=api_key, model=model)

    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "llama3")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
        return OllamaClient(model=model, base_url=base_url)

    raise ConfigurationError(
        f"Unsupported LLM_PROVIDER: '{provider}'. Choose 'groq', 'openai' or 'ollama'."
    )
