"""Local provider adapter for OpenAI-compatible local servers.

Supports Ollama, LM Studio, and similar local endpoints via the same adapter.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..provider_interface import ProviderInterface, ProviderResponse, ToolCall


class LocalProvider(ProviderInterface):
    """Unified local adapter using OpenAI-compatible chat completions."""

    @property
    def name(self) -> str:
        return "Local"

    def supports_vision(self) -> bool:
        return False

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _chat_completions_url(self) -> str:
        base_url = self.config.get("base_url", "http://127.0.0.1:1234/v1").rstrip("/")
        return f"{base_url}/chat/completions"

    def _models_url(self) -> str:
        base_url = self.config.get("base_url", "http://127.0.0.1:1234/v1").rstrip("/")
        return f"{base_url}/models"

    @staticmethod
    def _reachable_http_error(code: int) -> bool:
        return 400 <= code < 500

    def _probe(self, url: str, method: str = "GET") -> bool:
        req = Request(url, method=method, headers=self._headers())
        try:
            with urlopen(req, timeout=2):
                return True
        except HTTPError as exc:
            return self._reachable_http_error(exc.code)
        except Exception:
            return False

    def test_connection(self) -> bool:
        if self._probe(self._models_url(), method="GET"):
            return True
        if self._probe(self._chat_completions_url(), method="OPTIONS"):
            return True
        return self._probe(self._chat_completions_url(), method="GET")

    def generate_tool_calls(
        self,
        prompt: str,
        available_tools: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> ProviderResponse:
        payload = {
            "model": self.config.get("model", "local-model"),
            "messages": [
                {
                    "role": "system",
                    "content": "You are BlenderPilot. Use function tool calls to satisfy the user prompt.",
                },
                {"role": "user", "content": prompt},
            ],
            "tools": [
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
            "tool_choice": "auto",
            "max_tokens": max_tokens if max_tokens is not None else 1024,
            "temperature": 0.2 if temperature is None else temperature,
            "stream": False,
        }

        req = Request(
            self._chat_completions_url(),
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        try:
            with urlopen(req, timeout=60) as response:
                raw = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return ProviderResponse(
                [], None, f"Local provider request failed: HTTP {exc.code}"
            )
        except URLError as exc:
            return ProviderResponse(
                [], None, f"Local provider request failed: {exc.reason}"
            )
        except Exception as exc:
            return ProviderResponse([], None, f"Local provider request failed: {exc}")

        calls: List[ToolCall] = []
        try:
            tool_calls = raw["choices"][0]["message"].get("tool_calls") or []
            for call in tool_calls:
                fn = call.get("function", {})
                args = fn.get("arguments", {})
                if isinstance(args, str):
                    args = json.loads(args)
                calls.append(
                    ToolCall(
                        tool_name=fn["name"],
                        arguments=args,
                        id=call.get("id"),
                    )
                )
        except Exception as exc:
            return ProviderResponse([], raw, f"Local provider parsing failed: {exc}")

        if not calls:
            return ProviderResponse([], raw, "Local provider returned no tool calls")
        return ProviderResponse(calls, raw)
