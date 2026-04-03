"""MCP tool catalog for BlenderPilot.

The schemas are intentionally strict (additionalProperties=false) to support
fail-fast validation before any Blender operation runs.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _vector3_schema(default: List[float]) -> Dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 3,
        "maxItems": 3,
        "default": default,
    }


TOOLS: List[Dict[str, Any]] = [
    {
        "name": "create_cube",
        "description": "Create a cube mesh primitive",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "default": "Cube"},
                "location": _vector3_schema([0.0, 0.0, 0.0]),
                "scale": _vector3_schema([1.0, 1.0, 1.0]),
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
                "location": _vector3_schema([0.0, 0.0, 0.0]),
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
                "location": _vector3_schema([0.0, 0.0, 0.0]),
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
                "location": _vector3_schema([0.0, 0.0, 0.0]),
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
                "location": _vector3_schema([0.0, 0.0, 0.0]),
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
                "location": _vector3_schema([0.0, 0.0, 0.0]),
                "size": {"type": "number", "default": 2.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "set_location",
        "description": "Set object location",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "location": _vector3_schema([0.0, 0.0, 0.0]),
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
                "rotation": _vector3_schema([0.0, 0.0, 0.0]),
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
                "scale": _vector3_schema([1.0, 1.0, 1.0]),
            },
            "required": ["object_name", "scale"],
            "additionalProperties": False,
        },
    },
    {
        "name": "apply_material",
        "description": "Create/apply a simple Principled material on object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "material_name": {"type": "string", "default": "Material"},
                "base_color": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 4,
                    "maxItems": 4,
                    "default": [0.8, 0.8, 0.8, 1.0],
                },
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
                "base_color": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 4,
                    "maxItems": 4,
                    "default": [0.8, 0.8, 0.8, 1.0],
                },
                "metallic": {"type": "number", "default": 0.0},
                "roughness": {"type": "number", "default": 0.5},
                "emission_color": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 4,
                    "maxItems": 4,
                    "default": [0.0, 0.0, 0.0, 1.0],
                },
                "emission_strength": {"type": "number", "default": 0.0},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
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
                "location": _vector3_schema([0.0, 0.0, 5.0]),
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
                "location": _vector3_schema([0.0, -6.0, 4.0]),
                "rotation": _vector3_schema([1.0, 0.0, 0.0]),
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
                            "location": _vector3_schema([0.0, 0.0, 0.0]),
                            "scale": _vector3_schema([1.0, 1.0, 1.0]),
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
    {
        "name": "setup_scene",
        "description": "Quick scene setup with camera and one key light",
        "inputSchema": {
            "type": "object",
            "properties": {
                "camera_location": _vector3_schema([0.0, -6.0, 4.0]),
                "camera_rotation": _vector3_schema([1.0, 0.0, 0.0]),
                "light_location": _vector3_schema([3.0, -3.0, 5.0]),
                "light_energy": {"type": "number", "default": 1200.0},
            },
            "additionalProperties": False,
        },
    },
]


TOOLS_BY_NAME = {tool["name"]: tool for tool in TOOLS}


def get_tool_definitions() -> List[Dict[str, Any]]:
    """Return a copy-safe list of tool definitions."""
    return list(TOOLS)
