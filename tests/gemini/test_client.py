import asyncio
import json
from unittest.mock import AsyncMock, patch

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.llm.gemini_client import GeminiClient
from app.models.gemini_models import (
    Content,
    GenerateContentRequest,
    Role,
    TextPart,
    is_text_part,
)


@given(
    st.text(min_size=1, alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd")))
)
def test_build_url_property(method_name):
    """Property: _build_url should correctly include the method and API key."""
    api_key = "test-key"
    client = GeminiClient(api_key=api_key)
    url = client._build_url(method_name)
    assert f":{method_name}" in url
    assert f"key={api_key}" in url


@pytest.mark.asyncio
async def test_generate_content_success():
    """Verify unary content generation with mocked HTTP response."""
    expected_token_count = 10
    mock_response_data = {
        "candidates": [
            {"content": {"role": "model", "parts": [{"text": "Mocked response"}]}}
        ],
        "usageMetadata": {
            "promptTokenCount": 5,
            "candidatesTokenCount": 5,
            "totalTokenCount": expected_token_count,
        },
    }

    # Mock httpx response (httpx.Response.json is sync)
    from unittest.mock import Mock

    mock_resp = Mock()
    mock_resp.json.return_value = mock_response_data
    mock_resp.status_code = 200
    mock_resp.raise_for_status = Mock()

    with patch("httpx.AsyncClient.post", return_value=mock_resp):
        client = GeminiClient(api_key="fake-key")
        request = GenerateContentRequest(
            contents=[Content(role=Role.USER, parts=[TextPart(text="Hi")])]
        )

        response = await client.generate_content(request)

        first_part = response.candidates[0].content.parts[0]
        assert is_text_part(first_part)
        assert first_part.text == "Mocked response"

        assert response.usage_metadata is not None
        assert response.usage_metadata.total_token_count == expected_token_count
