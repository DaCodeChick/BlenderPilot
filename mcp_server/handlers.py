"""Tool execution handlers for BlenderPilot MCP server.

Handlers are written to run in two environments:
- Blender Python (with `bpy`) for real scene mutation
- Standard Python for development smoke tests (no-op simulation)
"""

from __future__ import annotations

from typing import Any, Dict, List


try:
    import bpy  # type: ignore
except Exception:  # pragma: no cover - exercised outside Blender
    bpy = None


class BlenderAdapter:
    """Thin adapter around bpy operations.

    When `bpy` is unavailable, operations return simulated results so the MCP
    bridge and validation logic can still be tested.
    """

    @property
    def available(self) -> bool:
        return bpy is not None

    def _lookup_object(self, name: str):
        if not self.available:
            return None
        return bpy.data.objects.get(name)

    def _rename_active(self, name: str) -> str:
        if not self.available:
            return name
        obj = bpy.context.active_object
        if obj and name:
            obj.name = name
            if obj.data:
                obj.data.name = f"{name}_Mesh"
        return obj.name if obj else name

    def create_cube(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Cube")
        location = args.get("location", [0.0, 0.0, 0.0])
        scale = args.get("scale", [1.0, 1.0, 1.0])
        if not self.available:
            return {"created": name, "kind": "cube", "simulated": True}
        bpy.ops.mesh.primitive_cube_add(location=location)
        obj_name = self._rename_active(name)
        obj = bpy.context.active_object
        obj.scale = scale
        return {"created": obj_name, "kind": "cube", "simulated": False}

    def create_sphere(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Sphere")
        location = args.get("location", [0.0, 0.0, 0.0])
        radius = args.get("radius", 1.0)
        if not self.available:
            return {"created": name, "kind": "sphere", "simulated": True}
        bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=radius)
        obj_name = self._rename_active(name)
        return {"created": obj_name, "kind": "sphere", "simulated": False}

    def create_cylinder(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Cylinder")
        location = args.get("location", [0.0, 0.0, 0.0])
        radius = args.get("radius", 1.0)
        depth = args.get("depth", 2.0)
        if not self.available:
            return {"created": name, "kind": "cylinder", "simulated": True}
        bpy.ops.mesh.primitive_cylinder_add(
            location=location, radius=radius, depth=depth
        )
        obj_name = self._rename_active(name)
        return {"created": obj_name, "kind": "cylinder", "simulated": False}

    def create_cone(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Cone")
        location = args.get("location", [0.0, 0.0, 0.0])
        radius = args.get("radius", 1.0)
        depth = args.get("depth", 2.0)
        if not self.available:
            return {"created": name, "kind": "cone", "simulated": True}
        bpy.ops.mesh.primitive_cone_add(location=location, radius1=radius, depth=depth)
        obj_name = self._rename_active(name)
        return {"created": obj_name, "kind": "cone", "simulated": False}

    def create_torus(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Torus")
        location = args.get("location", [0.0, 0.0, 0.0])
        major_radius = args.get("major_radius", 1.0)
        minor_radius = args.get("minor_radius", 0.25)
        if not self.available:
            return {"created": name, "kind": "torus", "simulated": True}
        bpy.ops.mesh.primitive_torus_add(
            location=location,
            major_radius=major_radius,
            minor_radius=minor_radius,
        )
        obj_name = self._rename_active(name)
        return {"created": obj_name, "kind": "torus", "simulated": False}

    def create_plane(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Plane")
        location = args.get("location", [0.0, 0.0, 0.0])
        size = args.get("size", 2.0)
        if not self.available:
            return {"created": name, "kind": "plane", "simulated": True}
        bpy.ops.mesh.primitive_plane_add(location=location, size=size)
        obj_name = self._rename_active(name)
        return {"created": obj_name, "kind": "plane", "simulated": False}

    def set_location(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args["object_name"]
        location = args["location"]
        if not self.available:
            return {"updated": name, "location": location, "simulated": True}
        obj = self._lookup_object(name)
        if not obj:
            raise ValueError(f"Object not found: {name}")
        obj.location = location
        return {"updated": name, "location": location, "simulated": False}

    def set_rotation(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args["object_name"]
        rotation = args["rotation"]
        if not self.available:
            return {"updated": name, "rotation": rotation, "simulated": True}
        obj = self._lookup_object(name)
        if not obj:
            raise ValueError(f"Object not found: {name}")
        obj.rotation_euler = rotation
        return {"updated": name, "rotation": rotation, "simulated": False}

    def set_scale(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args["object_name"]
        scale = args["scale"]
        if not self.available:
            return {"updated": name, "scale": scale, "simulated": True}
        obj = self._lookup_object(name)
        if not obj:
            raise ValueError(f"Object not found: {name}")
        obj.scale = scale
        return {"updated": name, "scale": scale, "simulated": False}

    def apply_material(self, args: Dict[str, Any]) -> Dict[str, Any]:
        object_name = args["object_name"]
        material_name = args.get("material_name", "Material")
        base_color = args.get("base_color", [0.8, 0.8, 0.8, 1.0])
        metallic = float(args.get("metallic", 0.0))
        roughness = float(args.get("roughness", 0.5))

        if not self.available:
            return {
                "updated": object_name,
                "material": material_name,
                "simulated": True,
            }

        obj = self._lookup_object(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")

        material = bpy.data.materials.get(material_name)
        if material is None:
            material = bpy.data.materials.new(name=material_name)
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = base_color
            bsdf.inputs["Metallic"].default_value = metallic
            bsdf.inputs["Roughness"].default_value = roughness

        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material

        return {
            "updated": object_name,
            "material": material_name,
            "simulated": False,
        }

    def build_material_graph(self, args: Dict[str, Any]) -> Dict[str, Any]:
        object_name = args["object_name"]
        material_name = args.get("material_name", "Material")
        base_color = args.get("base_color", [0.8, 0.8, 0.8, 1.0])
        metallic = float(args.get("metallic", 0.0))
        roughness = float(args.get("roughness", 0.5))
        emission_color = args.get("emission_color", [0.0, 0.0, 0.0, 1.0])
        emission_strength = float(args.get("emission_strength", 0.0))

        if not self.available:
            return {
                "updated": object_name,
                "material": material_name,
                "simulated": True,
            }

        obj = self._lookup_object(object_name)
        if not obj:
            raise ValueError(f"Object not found: {object_name}")

        material = bpy.data.materials.get(material_name)
        if material is None:
            material = bpy.data.materials.new(name=material_name)

        material.use_nodes = True
        node_tree = material.node_tree
        if not node_tree:
            raise ValueError("Material node tree unavailable")

        nodes = node_tree.nodes
        links = node_tree.links
        nodes.clear()

        out_node = nodes.new(type="ShaderNodeOutputMaterial")
        out_node.location = (300, 0)

        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.location = (0, 0)
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Emission Color"].default_value = emission_color
        bsdf.inputs["Emission Strength"].default_value = emission_strength

        links.new(bsdf.outputs["BSDF"], out_node.inputs["Surface"])

        if len(obj.data.materials) == 0:
            obj.data.materials.append(material)
        else:
            obj.data.materials[0] = material

        return {
            "updated": object_name,
            "material": material_name,
            "simulated": False,
        }

    def create_light(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Light")
        light_type = args.get("light_type", "POINT")
        location = args.get("location", [0.0, 0.0, 5.0])
        energy = args.get("energy", 1000.0)
        if not self.available:
            return {"created": name, "kind": "light", "simulated": True}
        light_data = bpy.data.lights.new(name=name, type=light_type)
        light_data.energy = energy
        light_object = bpy.data.objects.new(name, light_data)
        light_object.location = location
        bpy.context.collection.objects.link(light_object)
        return {"created": light_object.name, "kind": "light", "simulated": False}

    def create_camera(self, args: Dict[str, Any]) -> Dict[str, Any]:
        name = args.get("name", "Camera")
        location = args.get("location", [0.0, -6.0, 4.0])
        rotation = args.get("rotation", [1.0, 0.0, 0.0])
        if not self.available:
            return {"created": name, "kind": "camera", "simulated": True}
        cam_data = bpy.data.cameras.new(name)
        cam_obj = bpy.data.objects.new(name, cam_data)
        cam_obj.location = location
        cam_obj.rotation_euler = rotation
        bpy.context.collection.objects.link(cam_obj)
        bpy.context.scene.camera = cam_obj
        return {"created": cam_obj.name, "kind": "camera", "simulated": False}

    def create_primitive_group(self, args: Dict[str, Any]) -> Dict[str, Any]:
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
                created.append(self.create_cube(op_args))
            elif primitive == "sphere":
                created.append(self.create_sphere(op_args))
            elif primitive == "cylinder":
                created.append(self.create_cylinder(op_args))
            elif primitive == "cone":
                created.append(self.create_cone(op_args))
            elif primitive == "torus":
                created.append(self.create_torus(op_args))
            elif primitive == "plane":
                created.append(self.create_plane(op_args))
        return {"created": created, "count": len(created)}

    def setup_scene(self, args: Dict[str, Any]) -> Dict[str, Any]:
        camera_result = self.create_camera(
            {
                "name": "Camera",
                "location": args.get("camera_location", [0.0, -6.0, 4.0]),
                "rotation": args.get("camera_rotation", [1.0, 0.0, 0.0]),
            }
        )
        light_result = self.create_light(
            {
                "name": "KeyLight",
                "light_type": "AREA",
                "location": args.get("light_location", [3.0, -3.0, 5.0]),
                "energy": args.get("light_energy", 1200.0),
            }
        )
        return {"camera": camera_result, "light": light_result}


ADAPTER = BlenderAdapter()


def execute_tool(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a single MCP tool call by name."""
    if not hasattr(ADAPTER, name):
        raise ValueError(f"Unknown tool: {name}")
    method = getattr(ADAPTER, name)
    if not callable(method):
        raise ValueError(f"Tool is not callable: {name}")
    return method(args)
