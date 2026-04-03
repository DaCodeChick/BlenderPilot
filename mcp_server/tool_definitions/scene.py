"""Scene setup tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import vector3_schema


SCENE_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_light",
        "description": "Create a light object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Light"},
                "light_type": {
                    "type": "string",
                    "enum": ["POINT", "SUN", "SPOT", "AREA"],
                    "default": "POINT",
                },
                "location": vector3_schema([0.0, 0.0, 5.0]),
                "energy": {"type": "number", "default": 1000.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "create_camera",
        "description": "Create a camera object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Camera"},
                "location": vector3_schema([0.0, -6.0, 4.0]),
                "rotation": vector3_schema([1.0, 0.0, 0.0]),
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "setup_scene",
        "description": "Quick scene setup with camera and one key light",
        "inputSchema": {
            "type": "object",
            "properties": {
                "camera_location": vector3_schema([0.0, -6.0, 4.0]),
                "camera_rotation": vector3_schema([1.0, 0.0, 0.0]),
                "light_location": vector3_schema([3.0, -3.0, 5.0]),
                "light_energy": {"type": "number", "default": 1200.0},
            },
            "additionalProperties": False,
        },
    },
]
