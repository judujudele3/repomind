"""Groq LLM provider implementation.

Groq exposes an OpenAI-compatible API, so we reuse the openai SDK
with a custom base_url. No extra dependency needed.
"""
import logging

from openai import AsyncOpenAI

from app.core.base_llm import BaseLLM
from app.domain.exceptions import ProviderError

logger = logging.getLogger(__name__)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class GroqClient(BaseLLM):
    """Concrete implementation of BaseLLM using Groq (free, fast inference).

    Groq is OpenAI-API-compatible — we use the openai SDK
    pointed at Groq's endpoint. Zero extra dependencies.

    Recommended models:
    - llama-3.3-70b-versatile  (best quality, free)
    - llama-3.1-8b-instant     (fastest, lighter)
    - deepseek-r1-distill-llama-70b (reasoning)
    """

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile") -> None:
        self._model = model
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=GROQ_BASE_URL,
        )

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
                "Groq chat request",
                extra={"model": self._model, "message_count": len(messages)},
            )
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            raise ProviderError(f"Groq request failed: {exc}") from exc
