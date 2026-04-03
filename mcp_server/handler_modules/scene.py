"""Scene and camera/light handler functions."""

from __future__ import annotations

from typing import Any, Dict

from .context import CTX, bpy


def create_light(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Light")
    light_type = args.get("light_type", "POINT")
    location = args.get("location", [0.0, 0.0, 5.0])
    energy = args.get("energy", 1000.0)
    if not CTX.available:
        return {"created": name, "kind": "light", "simulated": True}
    light_data = bpy.data.lights.new(name=name, type=light_type)
    light_data.energy = energy
    light_object = bpy.data.objects.new(name, light_data)
    light_object.location = location
    bpy.context.collection.objects.link(light_object)
    return {"created": light_object.name, "kind": "light", "simulated": False}


def create_camera(args: Dict[str, Any]) -> Dict[str, Any]:
    name = args.get("name", "Camera")
    location = args.get("location", [0.0, -6.0, 4.0])
    rotation = args.get("rotation", [1.0, 0.0, 0.0])
    if not CTX.available:
        return {"created": name, "kind": "camera", "simulated": True}
    cam_data = bpy.data.cameras.new(name)
    cam_obj = bpy.data.objects.new(name, cam_data)
    cam_obj.location = location
    cam_obj.rotation_euler = rotation
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    return {"created": cam_obj.name, "kind": "camera", "simulated": False}


def setup_scene(args: Dict[str, Any]) -> Dict[str, Any]:
    camera_result = create_camera(
        {
            "name": "Camera",
            "location": args.get("camera_location", [0.0, -6.0, 4.0]),
            "rotation": args.get("camera_rotation", [1.0, 0.0, 0.0]),
        }
    )
    light_result = create_light(
        {
            "name": "KeyLight",
            "light_type": "AREA",
            "location": args.get("light_location", [3.0, -3.0, 5.0]),
            "energy": args.get("light_energy", 1200.0),
        }
    )
    return {"camera": camera_result, "light": light_result}
