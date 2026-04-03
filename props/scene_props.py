# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Scene-level properties for BlenderPilot UI state."""

import bpy
from bpy.types import PropertyGroup
from bpy.props import (
    StringProperty,
    BoolProperty,
    EnumProperty,
    CollectionProperty,
    IntProperty,
)


class BlenderPilotPromptHistoryItem(PropertyGroup):
    """A single prompt history item."""

    prompt: StringProperty(
        name="Prompt",
        description="Saved prompt text",
        default="",
        maxlen=4096,
    )

    provider: StringProperty(
        name="Provider",
        description="Provider used for this prompt",
        default="",
    )

    created_at: StringProperty(
        name="Created At",
        description="Timestamp for this prompt record",
        default="",
    )

    favorite: BoolProperty(
        name="Favorite",
        description="Whether this prompt is favorited",
        default=False,
    )


class BlenderPilotProperties(PropertyGroup):
    """Properties stored on the scene for UI state."""

    # User Prompt
    prompt: StringProperty(
        name="Prompt",
        description="Describe what you want to create in Blender",
        default="",
        maxlen=4096,
    )

    # Status
    status: StringProperty(
        name="Status",
        description="Current operation status",
        default="Ready",
    )

    is_generating: BoolProperty(
        name="Is Generating",
        description="Whether a generation is in progress",
        default=False,
    )

    last_error: StringProperty(
        name="Last Error",
        description="Last error message",
        default="",
    )

    # Provider Override (optional - defaults to preferences)
    use_provider_override: BoolProperty(
        name="Override Provider",
        description="Use a different provider than the one in preferences",
        default=False,
    )

    provider_override: EnumProperty(
        name="Provider Override",
        description="Which provider to use for this session",
        items=[
            ("openai", "OpenAI", "Use OpenAI API"),
            ("anthropic", "Anthropic", "Use Anthropic API"),
            ("local", "Local (Ollama/LM Studio)", "Use local OpenAI-compatible server"),
        ],
        default="openai",
    )

    prompt_history: CollectionProperty(
        name="Prompt History",
        description="History of submitted prompts",
        type=BlenderPilotPromptHistoryItem,
    )

    prompt_history_index: IntProperty(
        name="Prompt History Index",
        description="Active history item index",
        default=0,
        min=0,
    )


classes = (
    BlenderPilotPromptHistoryItem,
    BlenderPilotProperties,
)


def register():
    """Register scene properties."""
    for cls in classes:
        bpy.utils.register_class(cls)

    # Attach to scene
    bpy.types.Scene.blenderpilot = bpy.props.PointerProperty(
        type=BlenderPilotProperties
    )


def unregister():
    """Unregister scene properties."""
    # Remove from scene
    del bpy.types.Scene.blenderpilot

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
