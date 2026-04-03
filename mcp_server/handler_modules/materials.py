"""Material-related handler functions."""

from __future__ import annotations

from typing import Any, Dict

from .context import CTX, bpy


def apply_material(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    material_name = args.get("material_name", "Material")
    base_color = args.get("base_color", [0.8, 0.8, 0.8, 1.0])
    metallic = float(args.get("metallic", 0.0))
    roughness = float(args.get("roughness", 0.5))

    if not CTX.available:
        return {"updated": object_name, "material": material_name, "simulated": True}

    obj = CTX.lookup_object(object_name)
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

    return {"updated": object_name, "material": material_name, "simulated": False}


def build_material_graph(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    material_name = args.get("material_name", "Material")
    base_color = args.get("base_color", [0.8, 0.8, 0.8, 1.0])
    metallic = float(args.get("metallic", 0.0))
    roughness = float(args.get("roughness", 0.5))
    emission_color = args.get("emission_color", [0.0, 0.0, 0.0, 1.0])
    emission_strength = float(args.get("emission_strength", 0.0))

    if not CTX.available:
        return {"updated": object_name, "material": material_name, "simulated": True}

    obj = CTX.lookup_object(object_name)
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

    return {"updated": object_name, "material": material_name, "simulated": False}
