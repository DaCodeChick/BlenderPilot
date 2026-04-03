"""UV editing handlers."""

from __future__ import annotations

from typing import Any, Dict

from .context import CTX, bpy


def _ensure_edit_mesh_object(object_name: str):
    obj = CTX.lookup_object(object_name) if CTX.available else None
    if not obj:
        raise ValueError(f"Object not found: {object_name}")
    if obj.type != "MESH":
        raise ValueError(f"Object is not a mesh: {object_name}")
    bpy.context.view_layer.objects.active = obj
    if bpy.context.mode != "EDIT_MESH":
        bpy.ops.object.mode_set(mode="EDIT")
    return obj


def uv_unwrap(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    method = args.get("method", "ANGLE_BASED")
    if not CTX.available:
        return {"object": object_name, "method": method, "simulated": True}
    _ensure_edit_mesh_object(object_name)
    bpy.ops.uv.unwrap(method=method)
    return {"object": object_name, "method": method, "simulated": False}


def uv_smart_project(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    angle_limit = float(args.get("angle_limit", 66.0))
    island_margin = float(args.get("island_margin", 0.03))
    if not CTX.available:
        return {
            "object": object_name,
            "angle_limit": angle_limit,
            "island_margin": island_margin,
            "simulated": True,
        }
    _ensure_edit_mesh_object(object_name)
    bpy.ops.uv.smart_project(
        angle_limit=angle_limit,
        island_margin=island_margin,
    )
    return {
        "object": object_name,
        "angle_limit": angle_limit,
        "island_margin": island_margin,
        "simulated": False,
    }
