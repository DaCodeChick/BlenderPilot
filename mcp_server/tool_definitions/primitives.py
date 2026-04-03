"""Primitive modeling tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import vector3_schema


PRIMITIVE_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_cube",
        "description": "Create a cube mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Cube"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
                "scale": vector3_schema([1.0, 1.0, 1.0]),
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_sphere",
        "description": "Create a UV sphere mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Sphere"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
                "radius": {"type": "number", "default": 1.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_cylinder",
        "description": "Create a cylinder mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Cylinder"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
                "radius": {"type": "number", "default": 1.0},
                "depth": {"type": "number", "default": 2.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_cone",
        "description": "Create a cone mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Cone"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
                "radius": {"type": "number", "default": 1.0},
                "depth": {"type": "number", "default": 2.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_torus",
        "description": "Create a torus mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Torus"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
                "major_radius": {"type": "number", "default": 1.0},
                "minor_radius": {"type": "number", "default": 0.25},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_plane",
        "description": "Create a plane mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Plane"},
                "location": vector3_schema([0.0, 0.0, 0.0]),
                "size": {"type": "number", "default": 2.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_primitive_group",
        "description": "Create multiple primitives in one call",
        "inputSchema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "primitive": {
                                "type": "string",
                                "enum": [
                                    "cube",
                                    "sphere",
                                    "cylinder",
                                    "cone",
                                    "torus",
                                    "plane",
                                ],
                            },
                            "name": {"type": "string"},
                            "location": vector3_schema([0.0, 0.0, 0.0]),
                            "scale": vector3_schema([1.0, 1.0, 1.0]),
                        },
                        "required": ["primitive"],
                        "additionalProperties": False,
                    },
                    "minItems": 1,
                }
            },
            "required": ["items"],
            "additionalProperties": False,
        },
    },
]
