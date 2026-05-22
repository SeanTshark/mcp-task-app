from __future__ import annotations

import json
from collections.abc import AsyncGenerator

import httpx
from httpx_sse import aconnect_sse

from app.models.gemini_models import (
    GenerateContentRequest,
    GenerateContentResponse,
)

class GeminiClient:
    """
    An asynchronous client for the Gemini API.

    Handles both unary and streaming (SSE) content generation.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
    ):
        """
        Initialize the GeminiClient.

        Args:
            api_key: Your Google AI Studio API key.
            model_name: The Gemini model to use (e.g., 'gemini-2.5-flash').
            base_url: The base REST API URL.
        """
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")

    def _build_url(self, method: str) -> str:
        """Construct the REST URL for a specific model method."""
        return f"{self.base_url}/models/{self.model_name}:{method}?key={self.api_key}"
