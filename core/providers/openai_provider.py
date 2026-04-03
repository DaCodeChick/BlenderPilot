"""OpenAI provider adapter for MCP tool calling."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..provider_interface import ProviderInterface, ProviderResponse, ToolCall


class OpenAIProvider(ProviderInterface):
    """OpenAI adapter using Chat Completions tool calling."""

    @property
    def name(self) -> str:
        return "OpenAI"

    def supports_vision(self) -> bool:
        return True

    def test_connection(self) -> bool:
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=self.api_key)
            client.models.list()
            return True
        except Exception:
            return False

    def generate_tool_calls(
        self,
        prompt: str,
        available_tools: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        image_path: Optional[str] = None,
    ) -> ProviderResponse:
        try:
            from openai import OpenAI  # type: ignore
        except Exception as exc:
            return ProviderResponse([], None, f"OpenAI SDK unavailable: {exc}")

        model = self.config.get("model", "gpt-4.1-mini")
        max_completion_tokens = max_tokens if max_tokens is not None else 1024
        temp = 0.2 if temperature is None else temperature

        try:
            client = OpenAI(api_key=self.api_key)
            user_message: Dict[str, Any] = {"role": "user", "content": prompt}
            if image_path:
                p = Path(image_path)
                if not p.exists() or not p.is_file():
                    return ProviderResponse(
                        [], None, f"OpenAI image path not found: {image_path}"
                    )
                image_bytes = p.read_bytes()
                image_b64 = base64.b64encode(image_bytes).decode("ascii")
                user_message = {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                        },
                    ],
                }

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are BlenderPilot. Respond with tool calls only when possible. "
                            "Select tools that best satisfy the user prompt."
                        ),
                    },
                    user_message,
                ],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": tool["name"],
                            "description": tool["description"],
                            "parameters": tool["inputSchema"],
                        },
                    }
                    for tool in available_tools
                ],
                tool_choice="auto",
                max_completion_tokens=max_completion_tokens,
                temperature=temp,
            )
        except Exception as exc:
            return ProviderResponse([], None, f"OpenAI request failed: {exc}")

        calls: List[ToolCall] = []
        try:
            choice = response.choices[0]
            for call in choice.message.tool_calls or []:
                arguments = call.function.arguments
                if isinstance(arguments, str):
                    import json

                    arguments = json.loads(arguments)
                calls.append(
                    ToolCall(
                        tool_name=call.function.name,
                        arguments=arguments,
                        id=getattr(call, "id", None),
                    )
                )
        except Exception as exc:
            return ProviderResponse([], response, f"OpenAI parsing failed: {exc}")

        if not calls:
            return ProviderResponse([], response, "OpenAI returned no tool calls")
        return ProviderResponse(calls, response)
