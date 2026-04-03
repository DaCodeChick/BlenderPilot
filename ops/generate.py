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
    from ..core.provider_factory import create_provider  # type: ignore
    from ..core.sdk_installer import SDKInstaller  # type: ignore
    from ..core.validators import ToolCallValidator  # type: ignore
    from ..mcp_server.tools import get_tool_definitions  # type: ignore
except Exception:  # pragma: no cover
    from core.mcp_bridge import MCPBridge  # type: ignore
    from core.provider_factory import create_provider  # type: ignore
    from core.sdk_installer import SDKInstaller  # type: ignore
    from core.validators import ToolCallValidator  # type: ignore
    from mcp_server.tools import get_tool_definitions  # type: ignore


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
        addon_name = __package__.split(".")[0]
        prefs = context.preferences.addons[addon_name].preferences

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
            provider_name = (
                props.provider_override
                if props.use_provider_override
                else prefs.provider
            )

            if prefs.auto_install_sdks:
                ok, message = SDKInstaller.ensure_provider_sdk(provider_name)
                if not ok:
                    raise ValueError(message)

            provider = create_provider(provider_name, prefs)
            available_tools = get_tool_definitions()
            provider_response = provider.generate_tool_calls(
                prompt=prompt,
                available_tools=available_tools,
                max_tokens=prefs.max_tokens,
                temperature=prefs.temperature,
            )
            if not provider_response.success:
                raise ValueError(
                    provider_response.error or "Provider returned an unknown error"
                )

            bridge.initialize()
            bridge.list_tools()

            for call in provider_response.tool_calls:
                validation = validator.validate(call.tool_name, call.arguments)
                if not validation.valid:
                    raise ValueError(
                        validation.error or f"Invalid tool call: {call.tool_name}"
                    )
                bridge.call_tool(call.tool_name, call.arguments)

            props.status = f"Executed {len(provider_response.tool_calls)} tool call(s)"
            self.report(
                {"INFO"},
                f"MCP tool calls executed: {len(provider_response.tool_calls)}",
            )
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
