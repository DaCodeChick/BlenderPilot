"""Transform tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import vector3_schema


TRANSFORM_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "set_location",
        "description": "Set object location",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
            },
            "required": ["object_name", "location"],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_rotation",
        "description": "Set object rotation in radians",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "rotation": vector3_schema([0.0, 0.0, 0.0]),
            },
            "required": ["object_name", "rotation"],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_scale",
        "description": "Set object scale",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "scale": vector3_schema([1.0, 1.0, 1.0]),
            },
            "required": ["object_name", "scale"],
            "additionalProperties": False,
        },
    },
]
