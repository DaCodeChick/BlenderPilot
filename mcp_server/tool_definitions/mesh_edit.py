"""Mesh edit mode tool definitions."""

from __future__ import annotations

from typing import Any, Dict, List


MESH_EDIT_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "mesh_select_all",
        "description": "Select or deselect all mesh elements in edit mode",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "action": {
                    "type": "string",
                    "enum": ["SELECT", "DESELECT", "INVERT"],
                    "default": "SELECT",
                },
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mesh_extrude_region",
        "description": "Extrude selected region by offset vector",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "offset": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 3,
                    "maxItems": 3,
                    "default": [0.0, 0.0, 1.0],
                },
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mesh_bevel",
        "description": "Bevel selected mesh elements",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "offset": {"type": "number", "default": 0.05},
                "segments": {"type": "number", "default": 2},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mesh_inset",
        "description": "Inset selected faces",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "thickness": {"type": "number", "default": 0.02},
                "depth": {"type": "number", "default": 0.0},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mesh_mark_seam",
        "description": "Mark or clear UV seams on selected edges",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "clear": {"type": "boolean", "default": False},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
    {
        "name": "mesh_mark_sharp",
        "description": "Mark or clear sharp edges on selected edges",
        "inputSchema": {
            "type": "object",
            "properties": {
                "object_name": {"type": "string"},
                "clear": {"type": "boolean", "default": False},
            },
            "required": ["object_name"],
            "additionalProperties": False,
        },
    },
]
