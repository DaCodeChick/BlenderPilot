"""Composable MCP tool definition catalog."""

from __future__ import annotations

from typing import Any, Dict, List

from .materials import MATERIAL_TOOLS
from .primitives import PRIMITIVE_TOOLS
from .scene import SCENE_TOOLS
from .transforms import TRANSFORM_TOOLS


TOOLS: List[Dict[str, Any]] = [
    *PRIMITIVE_TOOLS,
    *TRANSFORM_TOOLS,
    *MATERIAL_TOOLS,
    *SCENE_TOOLS,
]

TOOLS_BY_NAME = {tool["name"]: tool for tool in TOOLS}


def get_tool_definitions() -> List[Dict[str, Any]]:
    return list(TOOLS)
