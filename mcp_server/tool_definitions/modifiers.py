"""Modifier tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List


MODIFIER_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "add_modifier",
        "description": "Add a modifier to an object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "modifier_name": {"type": "string", "default": "Modifier"},
                "modifier_type": {
                    "type": "string",
                    "enum": [
                        "SUBSURF",
                        "BEVEL",
                        "SOLIDIFY",
                        "ARRAY",
                        "MIRROR",
                        "DECIMATE",
                    ],
                },
            },
            "required": ["object_name", "modifier_type"],
            "additionalProperties": False,
        },
    },
    {
        "name": "configure_modifier",
        "description": "Configure common modifier properties",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "modifier_name": {"type": "string"},
                "levels": {"type": "number"},
                "render_levels": {"type": "number"},
                "width": {"type": "number"},
                "thickness": {"type": "number"},
                "count": {"type": "number"},
                "use_axis": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                },
            },
            "required": ["object_name", "modifier_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "apply_modifier",
        "description": "Apply a modifier on an object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "modifier_name": {"type": "string"},
            },
            "required": ["object_name", "modifier_name"],
            "additionalProperties": False,
        },
    },
]
