# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Addon preferences for API keys and settings."""

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, EnumProperty, BoolProperty


class BlenderPilotPreferences(AddonPreferences):
    """Preferences for BlenderPilot addon."""

    bl_idname = __package__.split(".")[0] if "." in __package__ else __package__

    # AI Provider Selection
    provider: EnumProperty(
        name="AI Provider",
        description="Select which AI provider to use",
        items=[
            ("openai", "OpenAI", "Use OpenAI API (GPT-4, etc.)"),
            ("anthropic", "Anthropic", "Use Anthropic API (Claude, etc.)"),
        ],
        default="openai",
    )

    # API Keys
    openai_api_key: StringProperty(
        name="OpenAI API Key",
        description="Your OpenAI API key (starts with sk-)",
        default="",
        subtype="PASSWORD",
    )

    anthropic_api_key: StringProperty(
        name="Anthropic API Key",
        description="Your Anthropic API key (starts with sk-ant-)",
        default="",
        subtype="PASSWORD",
    )

    # Advanced Settings
    use_env_file: BoolProperty(
        name="Use .env File",
        description="Load API keys from .env file in addon directory",
        default=True,
    )

    auto_install_sdks: BoolProperty(
        name="Auto-Install Provider SDKs",
        description="Automatically install provider SDKs (openai, anthropic) if missing",
        default=True,
    )

    max_tokens: bpy.props.IntProperty(
        name="Max Tokens",
        description="Maximum tokens for AI responses",
        default=4096,
        min=256,
        max=128000,
    )

    temperature: bpy.props.FloatProperty(
        name="Temperature",
        description="AI creativity level (0.0 = deterministic, 1.0 = creative)",
        default=0.7,
        min=0.0,
        max=2.0,
    )

    def draw(self, context):
        """Draw the preferences UI."""
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Provider Selection
        box = layout.box()
        box.label(text="AI Provider", icon="PREFERENCES")
        box.prop(self, "provider")

        # API Keys
        box = layout.box()
        box.label(text="API Keys", icon="LOCKED")
        box.prop(self, "openai_api_key")
        box.prop(self, "anthropic_api_key")
        box.prop(self, "use_env_file")

        if self.use_env_file:
            box.label(text="Note: .env file will override these keys", icon="INFO")

        # SDK Installation
        box = layout.box()
        box.label(text="SDK Installation", icon="PLUGIN")
        box.prop(self, "auto_install_sdks")

        if not self.auto_install_sdks:
            box.label(
                text="You must manually install: pip install openai anthropic",
                icon="ERROR",
            )

        # Advanced Settings
        box = layout.box()
        box.label(text="Advanced Settings", icon="SETTINGS")
        box.prop(self, "max_tokens")
        box.prop(self, "temperature")

        # Help
        box = layout.box()
        box.label(text="Documentation", icon="HELP")
        box.operator(
            "wm.url_open", text="View Documentation", icon="URL"
        ).url = "https://github.com/yourusername/BlenderPilot"


classes = (BlenderPilotPreferences,)


def register():
    """Register preferences."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister preferences."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
