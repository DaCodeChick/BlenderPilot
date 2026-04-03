"""Sculpting handlers."""

from __future__ import annotations

import math
from typing import Any, Dict

from .context import CTX, bpy


def _ensure_sculpt_mode_object(object_name: str):
    obj = CTX.lookup_object(object_name) if CTX.available else None
    if not obj:
        raise ValueError(f"Object not found: {object_name}")
    if obj.type != "MESH":
        raise ValueError(f"Object is not a mesh: {object_name}")
    bpy.context.view_layer.objects.active = obj
    if bpy.context.mode != "SCULPT":
        bpy.ops.object.mode_set(mode="SCULPT")
    return obj


def enter_sculpt_mode(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    if not CTX.available:
        return {"object": object_name, "mode": "SCULPT", "simulated": True}
    _ensure_sculpt_mode_object(object_name)
    return {"object": object_name, "mode": "SCULPT", "simulated": False}


def set_sculpt_brush(args: Dict[str, Any]) -> Dict[str, Any]:
    brush_name = args["brush_name"]
    if not CTX.available:
        return {"brush": brush_name, "simulated": True}

    brush = bpy.data.brushes.get(brush_name)
    if brush is None:
        raise ValueError(f"Brush not found: {brush_name}")

    tool_settings = bpy.context.tool_settings
    tool_settings.sculpt.brush = brush

    if "size" in args:
        tool_settings.unified_paint_settings.size = int(args["size"])
    if "strength" in args:
        tool_settings.unified_paint_settings.strength = float(args["strength"])
    if "use_frontface" in args and hasattr(brush, "use_frontface"):
        brush.use_frontface = bool(args["use_frontface"])

    return {
        "brush": brush_name,
        "size": getattr(tool_settings.unified_paint_settings, "size", None),
        "strength": getattr(tool_settings.unified_paint_settings, "strength", None),
        "simulated": False,
    }


def sculpt_face_set_from_mask(args: Dict[str, Any]) -> Dict[str, Any]:
    _ = args
    if not CTX.available:
        return {"operation": "face_set_from_mask", "simulated": True}
    bpy.ops.sculpt.face_sets_create(mode="MASKED")
    return {"operation": "face_set_from_mask", "simulated": False}


def sculpt_mask_flood_fill(args: Dict[str, Any]) -> Dict[str, Any]:
    mode = args.get("mode", "VALUE")
    value = float(args.get("value", 1.0))
    if not CTX.available:
        return {"mode": mode, "value": value, "simulated": True}
    bpy.ops.paint.mask_flood_fill(mode=mode, value=value)
    return {"mode": mode, "value": value, "simulated": False}


def sculpt_mesh_filter(args: Dict[str, Any]) -> Dict[str, Any]:
    filter_type = args.get("filter_type", "SMOOTH")
    strength = float(args.get("strength", 0.5))
    if not CTX.available:
        return {"filter": filter_type, "strength": strength, "simulated": True}
    bpy.ops.sculpt.mesh_filter(type=filter_type, strength=strength)
    return {"filter": filter_type, "strength": strength, "simulated": False}


def sculpt_symmetrize(args: Dict[str, Any]) -> Dict[str, Any]:
    direction = args.get("direction", "NEGATIVE_X")
    if not CTX.available:
        return {"direction": direction, "simulated": True}
    sculpt = bpy.context.tool_settings.sculpt
    sculpt.symmetrize_direction = direction
    bpy.ops.sculpt.symmetrize()
    return {"direction": direction, "simulated": False}


def _build_stroke(points, pressure: float, size: int):
    stroke = []
    for i, p in enumerate(points):
        stroke.append(
            {
                "name": "",
                "location": (float(p[0]), float(p[1]), float(p[2])),
                "mouse": (0.0, 0.0),
                "mouse_event": (0.0, 0.0),
                "pen_flip": False,
                "is_start": i == 0,
                "pressure": float(pressure),
                "size": int(size),
                "time": float(i),
                "x_tilt": 0.0,
                "y_tilt": 0.0,
            }
        )
    return stroke


def sculpt_brush_stroke_path(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    points = args["points"]
    pressure = float(args.get("pressure", 1.0))
    size = int(args.get("size", 40))

    if not CTX.available:
        return {
            "object": object_name,
            "points": len(points),
            "pressure": pressure,
            "size": size,
            "simulated": True,
        }

    _ensure_sculpt_mode_object(object_name)
    stroke = _build_stroke(points, pressure=pressure, size=size)
    bpy.ops.sculpt.brush_stroke(stroke=stroke, mode="NORMAL")
    return {
        "object": object_name,
        "points": len(points),
        "pressure": pressure,
        "size": size,
        "simulated": False,
    }


def sculpt_draw_line_stroke(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    start = args["start"]
    end = args["end"]
    steps = max(2, int(args.get("steps", 16)))
    pressure = float(args.get("pressure", 1.0))
    size = int(args.get("size", 40))

    points = []
    for i in range(steps):
        t = i / (steps - 1)
        points.append(
            [
                float(start[0]) * (1.0 - t) + float(end[0]) * t,
                float(start[1]) * (1.0 - t) + float(end[1]) * t,
                float(start[2]) * (1.0 - t) + float(end[2]) * t,
            ]
        )

    return sculpt_brush_stroke_path(
        {
            "object_name": object_name,
            "points": points,
            "pressure": pressure,
            "size": size,
        }
    )


def sculpt_voxel_remesh(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    voxel_size = float(args.get("voxel_size", 0.05))
    adaptivity = float(args.get("adaptivity", 0.0))
    fix_poles = bool(args.get("fix_poles", True))

    if not CTX.available:
        return {
            "object": object_name,
            "voxel_size": voxel_size,
            "adaptivity": adaptivity,
            "fix_poles": fix_poles,
            "simulated": True,
        }

    obj = _ensure_sculpt_mode_object(object_name)
    obj.data.remesh_voxel_size = max(0.0001, voxel_size)
    obj.data.remesh_voxel_adaptivity = max(0.0, adaptivity)
    obj.data.use_remesh_fix_poles = fix_poles
    bpy.ops.object.voxel_remesh()
    return {
        "object": object_name,
        "voxel_size": obj.data.remesh_voxel_size,
        "adaptivity": obj.data.remesh_voxel_adaptivity,
        "fix_poles": obj.data.use_remesh_fix_poles,
        "simulated": False,
    }
