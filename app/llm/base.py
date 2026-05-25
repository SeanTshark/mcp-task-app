from __future__ import annotations

from dataclasses import field
from typing import Any, Protocol

from pydantic.dataclasses import dataclass


class LLMProviderError(Exception):
    """Base exception for all LLM provider-related errors."""

    pass


@dataclass
class LLMRequest:
    """Provider-agnostic request model."""

    prompt: str
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """Provider-agnostic response model."""

    text: str
    raw_response: Any = None


class BaseLLMClient(Protocol):
    """
    Base contract for any LLM provider.

    All specific provider clients (Gemini, OpenAI, etc.) must implement
    this interface to ensure the rest of the application remains
    LLM-agnostic.
    """

    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response from the LLM based on the provided request."""
        ...
