"""Anthropic provider adapter for MCP-style tool calling."""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..provider_interface import ProviderInterface, ProviderResponse, ToolCall


class AnthropicProvider(ProviderInterface):
    """Anthropic adapter using Messages API tools."""

    @property
    def name(self) -> str:
        return "Anthropic"

    def supports_vision(self) -> bool:
        return True

    def test_connection(self) -> bool:
        try:
            import anthropic  # type: ignore

            client = anthropic.Anthropic(api_key=self.api_key)
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
            import anthropic  # type: ignore
        except Exception as exc:
            return ProviderResponse([], None, f"Anthropic SDK unavailable: {exc}")

        model = self.config.get("model", "claude-3-5-haiku-latest")
        max_out = max_tokens if max_tokens is not None else 1024
        temp = 0.2 if temperature is None else temperature

        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            user_content: Any = prompt
            if image_path:
                p = Path(image_path)
                if not p.exists() or not p.is_file():
                    return ProviderResponse(
                        [], None, f"Anthropic image path not found: {image_path}"
                    )
                image_b64 = base64.b64encode(p.read_bytes()).decode("ascii")
                user_content = [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_b64,
                        },
                    },
                ]

            response = client.messages.create(
                model=model,
                max_tokens=max_out,
                temperature=temp,
                system=(
                    "You are BlenderPilot. Use tools to satisfy the user prompt. "
                    "Prefer precise, minimal tool calls."
                ),
                messages=[{"role": "user", "content": user_content}],
                tools=[
                    {
                        "name": tool["name"],
                        "description": tool["description"],
                        "input_schema": tool["inputSchema"],
                    }
                    for tool in available_tools
                ],
            )
        except Exception as exc:
            return ProviderResponse([], None, f"Anthropic request failed: {exc}")

        calls: List[ToolCall] = []
        try:
            for block in response.content:
                if getattr(block, "type", None) == "tool_use":
                    calls.append(
                        ToolCall(
                            tool_name=block.name,
                            arguments=block.input,
                            id=getattr(block, "id", None),
                        )
                    )
        except Exception as exc:
            return ProviderResponse([], response, f"Anthropic parsing failed: {exc}")

        if not calls:
            return ProviderResponse([], response, "Anthropic returned no tool calls")
        return ProviderResponse(calls, response)
