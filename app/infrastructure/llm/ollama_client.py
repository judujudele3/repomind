"""Ollama LLM provider implementation (local inference)."""
import logging

import httpx

from app.core.base_llm import BaseLLM
from app.domain.exceptions import ProviderError

logger = logging.getLogger(__name__)


class OllamaClient(BaseLLM):
    """Concrete implementation of BaseLLM using Ollama (local)."""

    def __init__(
        self,
        model: str = "llama3",
        base_url: str = "http://ollama:11434",
    ) -> None:
        self._model = model
        self._base_url = base_url

    @property
    def model_name(self) -> str:
        return self._model

    async def complete(self, prompt: str, **kwargs) -> str:
        return await self.chat(
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )

    async def chat(self, messages: list[dict], **kwargs) -> str:
        try:
            logger.info(
                "Ollama chat request",
                model=self._model,
                message_count=len(messages),
            )
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._base_url}/api/chat",
                    json={
                        "model": self._model,
                        "messages": messages,
                        "stream": False,
                    },
                    timeout=120.0,
                )
                response.raise_for_status()
                data = response.json()
                return data["message"]["content"]
        except Exception as exc:
            raise ProviderError(f"Ollama request failed: {exc}") from exc
