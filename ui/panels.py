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
from pathlib import Path


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

        provider_name_map = {
            "openai": "OpenAI",
            "anthropic": "Anthropic",
            "local": "Local (Ollama/LM Studio)",
        }
        provider_name = provider_name_map.get(provider, provider)
        box.label(text=f"Provider: {provider_name}", icon="NETWORK_DRIVE")

        # Prompt Input
        layout.separator()
        layout.label(text="Prompt:", icon="TEXT")
        layout.prop(props, "prompt", text="")

        vision_box = layout.box()
        vision_box.label(text="Image Input", icon="IMAGE_DATA")
        vision_box.prop(props, "use_image_input", text="Enable Image Input")
        if props.use_image_input:
            vision_box.prop(props, "image_path", text="")
            exists = bool(props.image_path) and Path(props.image_path).exists()
            icon = "CHECKMARK" if exists else "ERROR"
            text = "Image ready" if exists else "Select a valid image file"
            vision_box.label(text=text, icon=icon)

        batch_row = layout.row(align=True)
        batch_row.prop(props, "batch_mode", text="Batch Mode")
        if props.batch_mode:
            batch_row.prop(props, "batch_max_items", text="Max")

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


class BLENDERPILOT_PT_history_panel(Panel):
    """Prompt history and favorites panel."""

    bl_label = "Prompt History"
    bl_idname = "BLENDERPILOT_PT_history_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BlenderPilot"
    bl_parent_id = "BLENDERPILOT_PT_main_panel"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout
        props = context.scene.blenderpilot

        if len(props.prompt_history) == 0:
            layout.label(text="No prompt history yet", icon="INFO")
            return

        col = layout.column(align=True)
        col.prop(props, "prompt_history_index", text="Selected")

        idx = props.prompt_history_index
        if 0 <= idx < len(props.prompt_history):
            item = props.prompt_history[idx]
            row = layout.row(align=True)
            row.label(text=f"Provider: {item.provider}", icon="NETWORK_DRIVE")
            icon = "SOLO_ON" if item.favorite else "SOLO_OFF"
            row.operator("blenderpilot.history_toggle_favorite", text="", icon=icon)

            layout.label(text=f"Saved: {item.created_at}", icon="TIME")
            layout.label(text=item.prompt[:120])

        row = layout.row(align=True)
        row.operator(
            "blenderpilot.history_load_prompt", text="Load Prompt", icon="IMPORT"
        )
        row.operator("blenderpilot.history_clear", text="Clear All", icon="TRASH")

        row = layout.row(align=True)
        op = row.operator(
            "blenderpilot.history_clear",
            text="Clear Favorites",
            icon="TRASH",
        )
        op.clear_favorites_only = True


classes = (
    BLENDERPILOT_PT_main_panel,
    BLENDERPILOT_PT_settings_panel,
    BLENDERPILOT_PT_history_panel,
)


def register():
    """Register UI panels."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister UI panels."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
