"""Minimal stdio JSON-RPC server for BlenderPilot MCP tools.

This process is intentionally transport-focused and keeps stdout reserved for
JSON-RPC responses only. Logs are emitted to stderr.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, Optional


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from mcp_server.handlers import execute_tool  # type: ignore
    from mcp_server.tools import get_tool_definitions  # type: ignore
else:
    from .handlers import execute_tool
    from .tools import get_tool_definitions


JSONRPC_VERSION = "2.0"


def _log(message: str) -> None:
    print(f"[blenderpilot-mcp] {message}", file=sys.stderr, flush=True)


def _response(result: Any, req_id: Any) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "result": result}


def _error(
    code: int, message: str, req_id: Any = None, data: Optional[Any] = None
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "jsonrpc": JSONRPC_VERSION,
        "id": req_id,
        "error": {"code": code, "message": message},
    }
    if data is not None:
        payload["error"]["data"] = data
    return payload


def _handle_request(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return _response(
            {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "blenderpilot-mcp", "version": "0.1.0"},
                "capabilities": {"tools": {}},
            },
            req_id,
        )

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return _response({"tools": get_tool_definitions()}, req_id)

    if method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        if not isinstance(arguments, dict):
            return _error(-32602, "Invalid params: arguments must be object", req_id)
        if not tool_name:
            return _error(-32602, "Invalid params: missing tool name", req_id)

        try:
            result = execute_tool(tool_name, arguments)
        except Exception as exc:
            return _error(-32000, f"Tool execution failed: {exc}", req_id)

        return _response(
            {"content": [{"type": "text", "text": json.dumps(result)}]}, req_id
        )

    return _error(-32601, f"Method not found: {method}", req_id)


def main() -> int:
    _log("server started")
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                payload = _error(-32600, "Invalid Request")
            else:
                payload = _handle_request(request)
            if payload is not None:
                sys.stdout.write(json.dumps(payload) + "\n")
                sys.stdout.flush()
        except json.JSONDecodeError:
            payload = _error(-32700, "Parse error")
            sys.stdout.write(json.dumps(payload) + "\n")
            sys.stdout.flush()
        except Exception as exc:  # pragma: no cover
            _log(f"fatal error: {exc}\n{traceback.format_exc()}")
            payload = _error(-32603, "Internal error")
            sys.stdout.write(json.dumps(payload) + "\n")
            sys.stdout.flush()
    _log("server stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
