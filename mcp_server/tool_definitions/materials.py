"""Material tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List

from .schema import color4_schema


def _vector_schema(default: List[float], size: int) -> Dict[str, Any]:
    return {
        "type": "array",
        "items": {"type": "number"},
        "minItems": size,
        "maxItems": size,
        "default": default,
    }


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
    {
        "name": "build_advanced_material_graph",
        "description": "Build an advanced preset material graph (glass, emissive, toon, layered)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "material_name": {"type": "string", "default": "AdvancedMaterial"},
                "preset": {
                    "type": "string",
                    "enum": ["glass", "emissive", "toon", "layered"],
                    "default": "glass",
                },
                "base_color": color4_schema([0.8, 0.8, 0.8, 1.0]),
                "accent_color": color4_schema([0.2, 0.6, 1.0, 1.0]),
                "metallic": {"type": "number", "default": 0.0},
                "roughness": {"type": "number", "default": 0.2},
                "ior": {"type": "number", "default": 1.45},
                "emission_strength": {"type": "number", "default": 4.0},
                "mix_factor": {"type": "number", "default": 0.35},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "add_material_node",
        "description": "Add a node to an existing material node tree",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "node_type": {"type": "string"},
                "node_name": {"type": "string", "default": ""},
                "location": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2,
                    "default": [0.0, 0.0],
                },
            },
            "required": ["material_name", "node_type"],
            "additionalProperties": False,
        },
    },
    {
        "name": "connect_material_nodes",
        "description": "Connect output socket from one node to input socket on another node",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "from_node": {"type": "string"},
                "from_socket": {"type": "string"},
                "to_node": {"type": "string"},
                "to_socket": {"type": "string"},
            },
            "required": [
                "material_name",
                "from_node",
                "from_socket",
                "to_node",
                "to_socket",
            ],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_material_node_float_input",
        "description": "Set a float input value on a material node",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "node_name": {"type": "string"},
                "input_name": {"type": "string"},
                "value": {"type": "number"},
            },
            "required": ["material_name", "node_name", "input_name", "value"],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_material_node_color_input",
        "description": "Set an RGBA input value on a material node",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "node_name": {"type": "string"},
                "input_name": {"type": "string"},
                "value": color4_schema([1.0, 1.0, 1.0, 1.0]),
            },
            "required": ["material_name", "node_name", "input_name", "value"],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_material_node_vector_input",
        "description": "Set a vector input value on a material node",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "node_name": {"type": "string"},
                "input_name": {"type": "string"},
                "value": _vector_schema([0.0, 0.0, 0.0], 3),
            },
            "required": ["material_name", "node_name", "input_name", "value"],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_material_node_texture_image",
        "description": "Assign an image file to an Image Texture node",
        "inputSchema": {
            "type": "object",
            "properties": {
                "material_name": {"type": "string"},
                "node_name": {"type": "string"},
                "image_path": {"type": "string"},
                "colorspace": {
                    "type": "string",
                    "enum": ["sRGB", "Non-Color"],
                    "default": "sRGB",
                },
            },
            "required": ["material_name", "node_name", "image_path"],
            "additionalProperties": False,
        },
    },
]
