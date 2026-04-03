"""Texture painting tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import color4_schema


TEXTURE_PAINT_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_texture_image",
        "description": "Create a generated image for texture painting",
        "inputSchema": {
            "type": "object",
            "properties": {
                "image_name": {"type": "string"},
                "width": {"type": "number", "default": 1024},
                "height": {"type": "number", "default": 1024},
                "color": color4_schema([1.0, 1.0, 1.0, 1.0]),
                "alpha": {"type": "boolean", "default": True},
            },
            "required": ["image_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "assign_texture_paint_image",
        "description": "Assign an image to an Image Texture node for paint target",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "node_name": {"type": "string"},
                "image_name": {"type": "string"},
            },
            "required": ["material_name", "node_name", "image_name"],
            "additionalProperties": False,
        },
    },
]
