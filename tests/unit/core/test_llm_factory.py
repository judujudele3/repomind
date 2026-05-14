"""Unit tests for LLM factory."""
import pytest

from app.domain.exceptions import ConfigurationError
from app.infrastructure.llm.factory import create_llm
from app.infrastructure.llm.groq_client import GroqClient
from app.infrastructure.llm.ollama_client import OllamaClient
from app.infrastructure.llm.openai_client import OpenAIClient


class TestLLMFactory:
    def test_creates_groq_client(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "groq")
        monkeypatch.setenv("GROQ_API_KEY", "gsk_test_key")
        monkeypatch.setenv("GROQ_MODEL", "llama-3.3-70b-versatile")

        llm = create_llm()
        assert isinstance(llm, GroqClient)
        assert llm.model_name == "llama-3.3-70b-versatile"

    def test_groq_is_default_provider(self, monkeypatch):
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        monkeypatch.setenv("GROQ_API_KEY", "gsk_test_key")

        llm = create_llm()
        assert isinstance(llm, GroqClient)

    def test_raises_on_missing_groq_key(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "groq")
        monkeypatch.delenv("GROQ_API_KEY", raising=False)

        with pytest.raises(ConfigurationError, match="GROQ_API_KEY"):
            create_llm()

    def test_creates_openai_client(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-key")
        monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")

        llm = create_llm()
        assert isinstance(llm, OpenAIClient)
        assert llm.model_name == "gpt-4o"

    def test_raises_on_missing_openai_key(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "openai")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)

        with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
            create_llm()

    def test_creates_ollama_client(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "ollama")
        monkeypatch.setenv("OLLAMA_MODEL", "llama3")

        llm = create_llm()
        assert isinstance(llm, OllamaClient)
        assert llm.model_name == "llama3"

    def test_raises_on_unknown_provider(self, monkeypatch):
        monkeypatch.setenv("LLM_PROVIDER", "anthropic")

        with pytest.raises(ConfigurationError, match="Unsupported LLM_PROVIDER"):
            create_llm()
