from __future__ import annotations

import asyncio
import os
from typing import Any

from dotenv import load_dotenv

from app.llm.gemini_client import GeminiClient
from app.models.gemini_models import (
    GenerateContentRequest,
    is_function_call_part,
    is_text_part,
)

load_dotenv()

# Basic Setup
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


def get_available_tools() -> list[dict[str, Any]]:
    """Define the tools available to Gemini."""
    return [
        {
            "function_declarations": [
                {
                    "name": "miles_to_kilometers",
                    "description": "Convert miles to kilometers",
                    "parameters": {
                        "type": "object",
                        "properties": {"miles": {"type": "number"}},
                        "required": ["miles"],
                    },
                }
            ]
        }
    ]


async def perform_initial_turn(
    client: GeminiClient, query: str
) -> tuple[list[Any], Any]:
    """Execute the first turn and return the message history and model response."""
    messages: list[Any] = [{"role": "user", "parts": [{"text": query}]}]
    tools = get_available_tools()

    print("\n[Thinking...]")
    response = await client.generate_content(
        GenerateContentRequest(contents=messages, tools=tools)  # type: ignore
    )
    return messages, response.candidates[0].content


def handle_manual_tool_call(call: Any) -> dict[str, Any]:
    """Prompt the user for manual tool execution and return the formatted response."""
    print(f"\n[Tool Requested: {call.name}]")
    print("\n--- ACTION REQUIRED ---")
    print(
        f"Run: curl -X POST http://localhost:8003/miles-to-kilometers -d '{call.args}'"
    )

    mcp_result = input("Enter the 'result' from the tool: ")

    return {
        "role": "model",
        "parts": [
            {
                "functionResponse": {
                    "name": call.name,
                    "response": {"result": mcp_result},
                }
            }
        ],
    }


async def run() -> None:
    """The main execution pipeline for the Gemini + MCP example."""
    if not API_KEY:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    client = GeminiClient(api_key=API_KEY, model_name=MODEL)

    print("--- Gemini MCP Simple Example ---")
    user_query = input("User: ")

    # 1. Start the conversation
    messages, model_turn = await perform_initial_turn(client, user_query)

    # 2. Process any tool requests
    for part in model_turn.parts:
        if is_function_call_part(part):
            tool_res_message = handle_manual_tool_call(part.function_call)

            messages.extend([model_turn.model_dump(by_alias=True), tool_res_message])

            # 3. Get the final explanation
            print("\n[Explaining...]")
            final_resp = await client.generate_content(
                GenerateContentRequest(contents=messages)
            )
            final_part = final_resp.candidates[0].content.parts[0]

            if is_text_part(final_part):
                print(f"\nGemini: {final_part.text}")
            return

    # If no tool was requested, just show the response
    if model_turn.parts and is_text_part(model_turn.parts[0]):
        print(f"\nGemini: {model_turn.parts[0].text}")


if __name__ == "__main__":
    asyncio.run(run())
