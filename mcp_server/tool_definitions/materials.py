"""Material tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import color4_schema


MATERIAL_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "apply_material",
        "description": "Create/apply a simple Principled material on object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "material_name": {"type": "string", "default": "Material"},
                "base_color": color4_schema([0.8, 0.8, 0.8, 1.0]),
                "metallic": {"type": "number", "default": 0.0},
                "roughness": {"type": "number", "default": 0.5},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "build_material_graph",
        "description": "Build a basic Principled shader graph and apply it",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "material_name": {"type": "string", "default": "Material"},
                "base_color": color4_schema([0.8, 0.8, 0.8, 1.0]),
                "metallic": {"type": "number", "default": 0.0},
                "roughness": {"type": "number", "default": 0.5},
                "emission_color": color4_schema([0.0, 0.0, 0.0, 1.0]),
                "emission_strength": {"type": "number", "default": 0.0},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
]
