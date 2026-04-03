# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""UI panels for BlenderPilot in the 3D View sidebar."""

import bpy
from bpy.types import Panel


class BLENDERPILOT_PT_main_panel(Panel):
    """Main BlenderPilot panel in 3D View sidebar."""

    bl_label = "BlenderPilot"
    bl_idname = "BLENDERPILOT_PT_main_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BlenderPilot"

    def draw(self, context):
        """Draw the main panel."""
        layout = self.layout
        scene = context.scene
        props = scene.blenderpilot
        prefs = context.preferences.addons[__package__.split(".")[0]].preferences

        # Status Box
        box = layout.box()
        if props.is_generating:
            box.label(text="Status: Generating...", icon="TIME")
        elif props.last_error:
            box.label(text="Status: Error", icon="ERROR")
            box.label(text=props.last_error, icon="NONE")
        else:
            box.label(text=f"Status: {props.status}", icon="CHECKMARK")

        # Provider Info
        box = layout.box()
        if props.use_provider_override:
            provider = props.provider_override
        else:
            provider = prefs.provider

        provider_name = "OpenAI" if provider == "openai" else "Anthropic"
        box.label(text=f"Provider: {provider_name}", icon="NETWORK_DRIVE")

        # Prompt Input
        layout.separator()
        layout.label(text="Prompt:", icon="TEXT")
        layout.prop(props, "prompt", text="")

        # Example Prompts
        box = layout.box()
        box.label(text="Example Prompts:", icon="LIGHTPROBE_GRID")
        col = box.column(align=True)
        col.scale_y = 0.8
        col.label(text="• Create a red cube")
        col.label(text="• Add a sphere with gold material")
        col.label(text="• Create a table with 4 legs")
        col.label(text="• Setup 3-point lighting")

        # Generate Button
        layout.separator()
        row = layout.row()
        row.scale_y = 2.0
        row.enabled = bool(props.prompt.strip()) and not props.is_generating
        row.operator("blenderpilot.generate", text="Generate", icon="PLAY")

        # Advanced Settings
        layout.separator()
        layout.prop(props, "use_provider_override", text="Override Provider")
        if props.use_provider_override:
            layout.prop(props, "provider_override", text="")


class BLENDERPILOT_PT_settings_panel(Panel):
    """Settings panel for BlenderPilot."""

    bl_label = "Settings"
    bl_idname = "BLENDERPILOT_PT_settings_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BlenderPilot"
    bl_parent_id = "BLENDERPILOT_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        """Draw the settings panel."""
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        prefs = context.preferences.addons[__package__.split(".")[0]].preferences

        # Quick access to key settings
        layout.prop(prefs, "max_tokens")
        layout.prop(prefs, "temperature")

        layout.separator()
        layout.operator(
            "preferences.addon_show", text="Open Full Preferences", icon="PREFERENCES"
        ).module = __package__.split(".")[0]


classes = (
    BLENDERPILOT_PT_main_panel,
    BLENDERPILOT_PT_settings_panel,
)


def register():
    """Register UI panels."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister UI panels."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
