"""OpenAI LLM provider implementation."""
import logging

from openai import AsyncOpenAI

from app.core.base_llm import BaseLLM
from app.domain.exceptions import ProviderError

logger = logging.getLogger(__name__)


class OpenAIClient(BaseLLM):
    """Concrete implementation of BaseLLM using OpenAI."""

    def __init__(self, api_key: str, model: str = "gpt-4o") -> None:
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key)

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
                "OpenAI chat request",
                model=self._model,
                message_count=len(messages),
            )
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            raise ProviderError(f"OpenAI request failed: {exc}") from exc
