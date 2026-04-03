"""Primitive and transform handler functions."""

from __future__ import annotations

from typing import Any, Dict, List

from .context import CTX, bpy


def create_cube(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Cube")
    location = args.get("location", [0.0, 0.0, 0.0])
    scale = args.get("scale", [1.0, 1.0, 1.0])
    if not CTX.available:
        return {"created": name, "kind": "cube", "simulated": True}
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj_name = CTX.rename_active(name)
    obj = bpy.context.active_object
    obj.scale = scale
    return {"created": obj_name, "kind": "cube", "simulated": False}


def create_sphere(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Sphere")
    location = args.get("location", [0.0, 0.0, 0.0])
    radius = args.get("radius", 1.0)
    if not CTX.available:
        return {"created": name, "kind": "sphere", "simulated": True}
    bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=radius)
    obj_name = CTX.rename_active(name)
    return {"created": obj_name, "kind": "sphere", "simulated": False}


def create_cylinder(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Cylinder")
    location = args.get("location", [0.0, 0.0, 0.0])
    radius = args.get("radius", 1.0)
    depth = args.get("depth", 2.0)
    if not CTX.available:
        return {"created": name, "kind": "cylinder", "simulated": True}
    bpy.ops.mesh.primitive_cylinder_add(location=location, radius=radius, depth=depth)
    obj_name = CTX.rename_active(name)
    return {"created": obj_name, "kind": "cylinder", "simulated": False}


def create_cone(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Cone")
    location = args.get("location", [0.0, 0.0, 0.0])
    radius = args.get("radius", 1.0)
    depth = args.get("depth", 2.0)
    if not CTX.available:
        return {"created": name, "kind": "cone", "simulated": True}
    bpy.ops.mesh.primitive_cone_add(location=location, radius1=radius, depth=depth)
    obj_name = CTX.rename_active(name)
    return {"created": obj_name, "kind": "cone", "simulated": False}


def create_torus(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Torus")
    location = args.get("location", [0.0, 0.0, 0.0])
    major_radius = args.get("major_radius", 1.0)
    minor_radius = args.get("minor_radius", 0.25)
    if not CTX.available:
        return {"created": name, "kind": "torus", "simulated": True}
    bpy.ops.mesh.primitive_torus_add(
        location=location,
        major_radius=major_radius,
        minor_radius=minor_radius,
    )
    obj_name = CTX.rename_active(name)
    return {"created": obj_name, "kind": "torus", "simulated": False}


def create_plane(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Plane")
    location = args.get("location", [0.0, 0.0, 0.0])
    size = args.get("size", 2.0)
    if not CTX.available:
        return {"created": name, "kind": "plane", "simulated": True}
    bpy.ops.mesh.primitive_plane_add(location=location, size=size)
    obj_name = CTX.rename_active(name)
    return {"created": obj_name, "kind": "plane", "simulated": False}


def set_location(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args["object_name"]
    location = args["location"]
    if not CTX.available:
        return {"updated": name, "location": location, "simulated": True}
    obj = CTX.lookup_object(name)
    if not obj:
        raise ValueError(f"Object not found: {name}")
    obj.location = location
    return {"updated": name, "location": location, "simulated": False}


def set_rotation(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args["object_name"]
    rotation = args["rotation"]
    if not CTX.available:
        return {"updated": name, "rotation": rotation, "simulated": True}
    obj = CTX.lookup_object(name)
    if not obj:
        raise ValueError(f"Object not found: {name}")
    obj.rotation_euler = rotation
    return {"updated": name, "rotation": rotation, "simulated": False}


def set_scale(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args["object_name"]
    scale = args["scale"]
    if not CTX.available:
        return {"updated": name, "scale": scale, "simulated": True}
    obj = CTX.lookup_object(name)
    if not obj:
        raise ValueError(f"Object not found: {name}")
    obj.scale = scale
    return {"updated": name, "scale": scale, "simulated": False}


def create_primitive_group(args: Dict[str, Any]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = args["items"]
    created = []
    for item in items:
        primitive = item["primitive"]
        op_args = {
            "name": item.get("name", primitive.capitalize()),
            "location": item.get("location", [0.0, 0.0, 0.0]),
            "scale": item.get("scale", [1.0, 1.0, 1.0]),
        }
        if primitive == "cube":
            created.append(create_cube(op_args))
        elif primitive == "sphere":
            created.append(create_sphere(op_args))
        elif primitive == "cylinder":
            created.append(create_cylinder(op_args))
        elif primitive == "cone":
            created.append(create_cone(op_args))
        elif primitive == "torus":
            created.append(create_torus(op_args))
        elif primitive == "plane":
            created.append(create_plane(op_args))
    return {"created": created, "count": len(created)}
