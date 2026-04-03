"""Shared schema builders for MCP tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List


def vector3_schema(default: List[float]) -> Dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 3,
        "maxItems": 3,
        "default": default,
    }


def color4_schema(default: List[float]) -> Dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 4,
        "maxItems": 4,
        "default": default,
    }
