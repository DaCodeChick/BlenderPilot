"""Sculpting tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List


SCULPT_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "enter_sculpt_mode",
        "description": "Set active mesh object into sculpt mode",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "set_sculpt_brush",
        "description": "Set active sculpt brush and common brush settings",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brush_name": {"type": "string"},
                "size": {"type": "number"},
                "strength": {"type": "number"},
                "use_frontface": {"type": "boolean"},
            },
            "required": ["brush_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_face_set_from_mask",
        "description": "Create face sets from current mask",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_mask_flood_fill",
        "description": "Flood fill mask with value",
        "inputSchema": {
            "type": "object",
            "properties": {
                "mode": {
                    "type": "string",
                    "enum": ["VALUE", "INVERT", "VALUE_INVERSE"],
                    "default": "VALUE",
                },
                "value": {"type": "number", "default": 1.0},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_mesh_filter",
        "description": "Apply sculpt mesh filter operation",
        "inputSchema": {
            "type": "object",
            "properties": {
                "filter_type": {
                    "type": "string",
                    "enum": [
                        "SMOOTH",
                        "SCALE",
                        "INFLATE",
                        "SPHERE",
                        "RANDOM",
                        "RELAX",
                        "RELAX_FACE_SETS",
                        "SURFACE_SMOOTH",
                        "SHARPEN",
                        "ENHANCE_DETAILS",
                        "ERASE_DISPLACEMENT",
                    ],
                    "default": "SMOOTH",
                },
                "strength": {"type": "number", "default": 0.5},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_symmetrize",
        "description": "Symmetrize sculpt mesh across axis",
        "inputSchema": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": [
                        "NEGATIVE_X",
                        "POSITIVE_X",
                        "NEGATIVE_Y",
                        "POSITIVE_Y",
                        "NEGATIVE_Z",
                        "POSITIVE_Z",
                    ],
                    "default": "NEGATIVE_X",
                }
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_brush_stroke_path",
        "description": "Apply sculpt brush strokes along a 3D point path",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "points": {
                    "type": "array",
                    "minItems": 2,
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 3,
                        "maxItems": 3,
                    },
                },
                "pressure": {"type": "number", "default": 1.0},
                "size": {"type": "number", "default": 40},
            },
            "required": ["object_name", "points"],
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_draw_line_stroke",
        "description": "Draw a sculpt stroke from start to end using interpolated points",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "start": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                },
                "end": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                },
                "steps": {"type": "number", "default": 16},
                "pressure": {"type": "number", "default": 1.0},
                "size": {"type": "number", "default": 40},
            },
            "required": ["object_name", "start", "end"],
            "additionalProperties": False,
        },
    },
    {
        "name": "sculpt_voxel_remesh",
        "description": "Perform voxel remesh on sculpt object",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "voxel_size": {"type": "number", "default": 0.05},
                "adaptivity": {"type": "number", "default": 0.0},
                "fix_poles": {"type": "boolean", "default": True},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
]
