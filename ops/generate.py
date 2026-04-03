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
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences

        # Get prompt
        prompt = props.prompt.strip()
        if not prompt:
            self.report({"ERROR"}, "Please enter a prompt")
            return {"CANCELLED"}

        # Get provider
        if props.use_provider_override:
            provider = props.provider_override
        else:
            provider = prefs.provider

        # TODO: Implement actual generation
        # For now, just show a message
        props.status = f"Would generate with {provider}: {prompt[:50]}..."
        props.last_error = ""

        self.report({"INFO"}, f"Generation stub: {prompt[:50]}...")

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
