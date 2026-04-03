"""Subprocess bridge for communicating with BlenderPilot MCP server."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Optional


class MCPBridge:
    """Manage a stdio subprocess running the local MCP server."""

    def __init__(self) -> None:
        self.process: Optional[subprocess.Popen[str]] = None
        self._request_id = 0

    def _server_script(self) -> Path:
        return Path(__file__).resolve().parents[1] / "mcp_server" / "main.py"

    def is_running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self) -> None:
        if self.is_running():
            return
        script_path = self._server_script()
        self.process = subprocess.Popen(
            [sys.executable, str(script_path)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
        )

    def stop(self) -> None:
        if not self.process:
            return
        if self.is_running():
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.process = None

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _rpc(
        self, method: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        self.start()
        if not self.process or not self.process.stdin or not self.process.stdout:
            raise RuntimeError("MCP server process is not available")

        payload: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
        }
        if params is not None:
            payload["params"] = params

        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()

        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("No response from MCP server")
        response = json.loads(line)
        if "error" in response:
            message = response["error"].get("message", "Unknown MCP error")
            raise RuntimeError(message)
        return response["result"]

    def initialize(self) -> Dict[str, Any]:
        return self._rpc(
            "initialize",
            {"clientInfo": {"name": "blenderpilot-addon", "version": "0.1.0"}},
        )

    def list_tools(self) -> Dict[str, Any]:
        return self._rpc("tools/list")

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        return self._rpc("tools/call", {"name": name, "arguments": arguments})
