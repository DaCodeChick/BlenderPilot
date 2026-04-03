"""Composable MCP tool definition catalog."""

from __future__ import annotations

from typing import Any, Dict, List

from .materials import MATERIAL_TOOLS
from .mesh_edit import MESH_EDIT_TOOLS
from .modifiers import MODIFIER_TOOLS
from .primitives import PRIMITIVE_TOOLS
from .scene import SCENE_TOOLS
from .texture_paint import TEXTURE_PAINT_TOOLS
from .transforms import TRANSFORM_TOOLS
from .uv import UV_TOOLS


TOOLS: List[Dict[str, Any]] = [
    *PRIMITIVE_TOOLS,
    *TRANSFORM_TOOLS,
    *MESH_EDIT_TOOLS,
    *MODIFIER_TOOLS,
    *UV_TOOLS,
    *TEXTURE_PAINT_TOOLS,
    *MATERIAL_TOOLS,
    *SCENE_TOOLS,
]

TOOLS_BY_NAME = {tool["name"]: tool for tool in TOOLS}


def get_tool_definitions() -> List[Dict[str, Any]]:
    return list(TOOLS)
