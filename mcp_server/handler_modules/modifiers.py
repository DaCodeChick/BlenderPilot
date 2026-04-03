"""Modifier handlers."""

from __future__ import annotations

from typing import Any, Dict

from .context import CTX, bpy


def add_modifier(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    modifier_type = args["modifier_type"]
    modifier_name = args.get("modifier_name", modifier_type.title())

    if not CTX.available:
        return {
            "object": object_name,
            "modifier": modifier_name,
            "type": modifier_type,
            "simulated": True,
        }

    obj = CTX.lookup_object(object_name)
    if not obj:
        raise ValueError(f"Object not found: {object_name}")
    mod = obj.modifiers.new(name=modifier_name, type=modifier_type)
    return {
        "object": object_name,
        "modifier": mod.name,
        "type": mod.type,
        "simulated": False,
    }


def configure_modifier(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    modifier_name = args["modifier_name"]

    if not CTX.available:
        return {
            "object": object_name,
            "modifier": modifier_name,
            "configured": True,
            "simulated": True,
        }

    obj = CTX.lookup_object(object_name)
    if not obj:
        raise ValueError(f"Object not found: {object_name}")
    mod = obj.modifiers.get(modifier_name)
    if not mod:
        raise ValueError(f"Modifier not found: {modifier_name}")

    if "levels" in args and hasattr(mod, "levels"):
        mod.levels = int(args["levels"])
    if "render_levels" in args and hasattr(mod, "render_levels"):
        mod.render_levels = int(args["render_levels"])
    if "width" in args and hasattr(mod, "width"):
        mod.width = float(args["width"])
    if "thickness" in args and hasattr(mod, "thickness"):
        mod.thickness = float(args["thickness"])
    if "count" in args and hasattr(mod, "count"):
        mod.count = int(args["count"])
    if "use_axis" in args and hasattr(mod, "use_axis"):
        axis = args["use_axis"]
        mod.use_axis[0] = bool(axis[0])
        mod.use_axis[1] = bool(axis[1])
        mod.use_axis[2] = bool(axis[2])

    return {
        "object": object_name,
        "modifier": modifier_name,
        "configured": True,
        "simulated": False,
    }


def apply_modifier(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    modifier_name = args["modifier_name"]

    if not CTX.available:
        return {
            "object": object_name,
            "modifier": modifier_name,
            "applied": True,
            "simulated": True,
        }

    obj = CTX.lookup_object(object_name)
    if not obj:
        raise ValueError(f"Object not found: {object_name}")

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.modifier_apply(modifier=modifier_name)
    return {
        "object": object_name,
        "modifier": modifier_name,
        "applied": True,
        "simulated": False,
    }
