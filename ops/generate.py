# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Main generation operator for BlenderPilot."""

import bpy
from bpy.types import Operator

try:
    from ..core.mcp_bridge import MCPBridge  # type: ignore
    from ..core.validators import ToolCallValidator  # type: ignore
except Exception:  # pragma: no cover
    from core.mcp_bridge import MCPBridge  # type: ignore
    from core.validators import ToolCallValidator  # type: ignore


def _plan_tool_call_from_prompt(prompt: str):
    """Very small phase-2 planner until provider integration lands."""
    text = prompt.lower()
    if "sphere" in text:
        return "create_sphere", {
            "name": "Sphere",
            "location": [0.0, 0.0, 0.0],
            "radius": 1.0,
        }
    if "cylinder" in text:
        return "create_cylinder", {
            "name": "Cylinder",
            "location": [0.0, 0.0, 0.0],
            "radius": 1.0,
            "depth": 2.0,
        }
    if "cone" in text:
        return "create_cone", {
            "name": "Cone",
            "location": [0.0, 0.0, 0.0],
            "radius": 1.0,
            "depth": 2.0,
        }
    if "torus" in text:
        return "create_torus", {
            "name": "Torus",
            "location": [0.0, 0.0, 0.0],
            "major_radius": 1.0,
            "minor_radius": 0.25,
        }
    if "plane" in text:
        return "create_plane", {
            "name": "Plane",
            "location": [0.0, 0.0, 0.0],
            "size": 2.0,
        }
    if "light" in text:
        return "create_light", {
            "name": "KeyLight",
            "light_type": "AREA",
            "location": [3.0, -3.0, 5.0],
            "energy": 1200.0,
        }
    if "camera" in text:
        return "create_camera", {
            "name": "Camera",
            "location": [0.0, -6.0, 4.0],
            "rotation": [1.0, 0.0, 0.0],
        }
    if "scene" in text:
        return "setup_scene", {}
    return "create_cube", {
        "name": "Cube",
        "location": [0.0, 0.0, 0.0],
        "scale": [1.0, 1.0, 1.0],
    }


class BLENDERPILOT_OT_generate(Operator):
    """Generate Blender content from AI prompt."""

    bl_idname = "blenderpilot.generate"
    bl_label = "Generate"
    bl_description = "Generate Blender content based on your prompt"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        """Check if operator can run."""
        props = context.scene.blenderpilot
        return bool(props.prompt.strip()) and not props.is_generating

    def execute(self, context):
        """Execute the generation."""
        scene = context.scene
        props = scene.blenderpilot

        # Get prompt
        prompt = props.prompt.strip()
        if not prompt:
            self.report({"ERROR"}, "Please enter a prompt")
            return {"CANCELLED"}

        props.is_generating = True
        props.last_error = ""
        props.status = "Starting MCP generation..."

        bridge = MCPBridge()
        validator = ToolCallValidator()

        try:
            bridge.initialize()
            bridge.list_tools()

            tool_name, arguments = _plan_tool_call_from_prompt(prompt)
            validation = validator.validate(tool_name, arguments)
            if not validation.valid:
                raise ValueError(validation.error or "Invalid tool call")

            result = bridge.call_tool(tool_name, arguments)
            props.status = f"Executed {tool_name} successfully"
            self.report({"INFO"}, f"MCP tool executed: {tool_name}")
            if result:
                _ = result
        except Exception as exc:
            props.last_error = str(exc)
            props.status = "Generation failed"
            self.report({"ERROR"}, f"BlenderPilot error: {exc}")
            return {"CANCELLED"}
        finally:
            props.is_generating = False
            bridge.stop()

        return {"FINISHED"}


classes = (BLENDERPILOT_OT_generate,)


def register():
    """Register operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
