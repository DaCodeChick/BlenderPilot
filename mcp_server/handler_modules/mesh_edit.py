"""Mesh edit mode handlers."""

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


def mesh_select_all(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    action = args.get("action", "SELECT")
    if not CTX.available:
        return {"object": object_name, "action": action, "simulated": True}
    _ensure_edit_mesh_object(object_name)
    bpy.ops.mesh.select_all(action=action)
    return {"object": object_name, "action": action, "simulated": False}


def mesh_extrude_region(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    offset = args.get("offset", [0.0, 0.0, 1.0])
    if not CTX.available:
        return {"object": object_name, "offset": offset, "simulated": True}
    _ensure_edit_mesh_object(object_name)
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": (float(offset[0]), float(offset[1]), float(offset[2]))
        }
    )
    return {"object": object_name, "offset": offset, "simulated": False}


def mesh_bevel(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    offset = float(args.get("offset", 0.05))
    segments = int(args.get("segments", 2))
    if not CTX.available:
        return {
            "object": object_name,
            "offset": offset,
            "segments": segments,
            "simulated": True,
        }
    _ensure_edit_mesh_object(object_name)
    bpy.ops.mesh.bevel(offset=offset, segments=max(1, segments))
    return {
        "object": object_name,
        "offset": offset,
        "segments": segments,
        "simulated": False,
    }


def mesh_inset(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    thickness = float(args.get("thickness", 0.02))
    depth = float(args.get("depth", 0.0))
    if not CTX.available:
        return {
            "object": object_name,
            "thickness": thickness,
            "depth": depth,
            "simulated": True,
        }
    _ensure_edit_mesh_object(object_name)
    bpy.ops.mesh.inset(thickness=thickness, depth=depth)
    return {
        "object": object_name,
        "thickness": thickness,
        "depth": depth,
        "simulated": False,
    }


def mesh_mark_seam(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    clear = bool(args.get("clear", False))
    if not CTX.available:
        return {"object": object_name, "clear": clear, "simulated": True}
    _ensure_edit_mesh_object(object_name)
    bpy.ops.mesh.mark_seam(clear=clear)
    return {"object": object_name, "clear": clear, "simulated": False}


def mesh_mark_sharp(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    clear = bool(args.get("clear", False))
    if not CTX.available:
        return {"object": object_name, "clear": clear, "simulated": True}
    _ensure_edit_mesh_object(object_name)
    bpy.ops.mesh.mark_sharp(clear=clear)
    return {"object": object_name, "clear": clear, "simulated": False}
