"""Operators for prompt history and favorites."""

from __future__ import annotations

import bpy
from bpy.types import Operator


class BLENDERPILOT_OT_history_load_prompt(Operator):
    """Load selected history item into prompt input."""

    bl_idname = "blenderpilot.history_load_prompt"
    bl_label = "Load Prompt"
    bl_description = "Load selected prompt from history"

    @classmethod
    def poll(cls, context):
        props = context.scene.blenderpilot
        return len(props.prompt_history) > 0

    def execute(self, context):
        props = context.scene.blenderpilot
        idx = props.prompt_history_index
        if idx < 0 or idx >= len(props.prompt_history):
            self.report({"ERROR"}, "No history item selected")
            return {"CANCELLED"}
        props.prompt = props.prompt_history[idx].prompt
        self.report({"INFO"}, "Loaded prompt from history")
        return {"FINISHED"}


class BLENDERPILOT_OT_history_toggle_favorite(Operator):
    """Toggle favorite on selected history item."""

    bl_idname = "blenderpilot.history_toggle_favorite"
    bl_label = "Toggle Favorite"
    bl_description = "Toggle favorite for selected prompt"

    @classmethod
    def poll(cls, context):
        props = context.scene.blenderpilot
        return len(props.prompt_history) > 0

    def execute(self, context):
        props = context.scene.blenderpilot
        idx = props.prompt_history_index
        if idx < 0 or idx >= len(props.prompt_history):
            self.report({"ERROR"}, "No history item selected")
            return {"CANCELLED"}

        item = props.prompt_history[idx]
        item.favorite = not item.favorite
        state = "favorited" if item.favorite else "unfavorited"
        self.report({"INFO"}, f"Prompt {state}")
        return {"FINISHED"}


class BLENDERPILOT_OT_history_clear(Operator):
    """Clear prompt history."""

    bl_idname = "blenderpilot.history_clear"
    bl_label = "Clear History"
    bl_description = "Remove all prompt history entries"

    clear_favorites_only: bpy.props.BoolProperty(
        name="Clear Favorites Only",
        default=False,
    )

    def execute(self, context):
        props = context.scene.blenderpilot

        if self.clear_favorites_only:
            keep = [
                {
                    "prompt": item.prompt,
                    "provider": item.provider,
                    "created_at": item.created_at,
                    "favorite": item.favorite,
                }
                for item in props.prompt_history
                if not item.favorite
            ]
            props.prompt_history.clear()
            for row in keep:
                item = props.prompt_history.add()
                item.prompt = row["prompt"]
                item.provider = row["provider"]
                item.created_at = row["created_at"]
                item.favorite = row["favorite"]
            props.prompt_history_index = min(
                props.prompt_history_index, max(0, len(props.prompt_history) - 1)
            )
            self.report({"INFO"}, "Cleared favorited prompts")
            return {"FINISHED"}

        props.prompt_history.clear()
        props.prompt_history_index = 0
        self.report({"INFO"}, "Cleared prompt history")
        return {"FINISHED"}


classes = (
    BLENDERPILOT_OT_history_load_prompt,
    BLENDERPILOT_OT_history_toggle_favorite,
    BLENDERPILOT_OT_history_clear,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
