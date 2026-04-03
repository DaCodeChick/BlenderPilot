"""Compatibility wrapper for modular MCP tool handlers."""

from __future__ import annotations

from typing import Any, Dict

from .handler_modules import HANDLERS


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a single MCP tool call by name."""
    handler = HANDLERS.get(name)
    if handler is None:
        raise ValueError(f"Unknown tool: {name}")
    return handler(args)
