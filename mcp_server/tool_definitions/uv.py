"""UV editing tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List


UV_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "uv_unwrap",
        "description": "Unwrap mesh UVs in edit mode",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "method": {
                    "type": "string",
                    "enum": ["ANGLE_BASED", "CONFORMAL"],
                    "default": "ANGLE_BASED",
                },
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "uv_smart_project",
        "description": "Smart UV project for selected mesh",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "angle_limit": {"type": "number", "default": 66.0},
                "island_margin": {"type": "number", "default": 0.03},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
]
