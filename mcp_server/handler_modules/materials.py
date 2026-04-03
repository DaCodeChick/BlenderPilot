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


def build_advanced_material_graph(args: Dict[str, Any]) -> Dict[str, Any]:
    object_name = args["object_name"]
    material_name = args.get("material_name", "AdvancedMaterial")
    preset = args.get("preset", "glass")
    base_color = args.get("base_color", [0.8, 0.8, 0.8, 1.0])
    accent_color = args.get("accent_color", [0.2, 0.6, 1.0, 1.0])
    metallic = float(args.get("metallic", 0.0))
    roughness = float(args.get("roughness", 0.2))
    ior = float(args.get("ior", 1.45))
    emission_strength = float(args.get("emission_strength", 4.0))
    mix_factor = float(args.get("mix_factor", 0.35))

    if not CTX.available:
        return {
            "updated": object_name,
            "material": material_name,
            "preset": preset,
            "simulated": True,
        }

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
    out_node.location = (700, 0)

    if preset == "glass":
        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.location = (350, 0)
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Roughness"].default_value = max(0.0, min(roughness, 1.0))
        bsdf.inputs["IOR"].default_value = max(1.0, ior)
        bsdf.inputs["Transmission Weight"].default_value = 1.0
        links.new(bsdf.outputs["BSDF"], out_node.inputs["Surface"])

    elif preset == "emissive":
        emission = nodes.new(type="ShaderNodeEmission")
        emission.location = (350, 100)
        emission.inputs["Color"].default_value = accent_color
        emission.inputs["Strength"].default_value = max(0.0, emission_strength)

        bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        bsdf.location = (350, -120)
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Roughness"].default_value = max(0.0, min(roughness, 1.0))

        add = nodes.new(type="ShaderNodeAddShader")
        add.location = (520, 0)
        links.new(emission.outputs["Emission"], add.inputs[0])
        links.new(bsdf.outputs["BSDF"], add.inputs[1])
        links.new(add.outputs["Shader"], out_node.inputs["Surface"])

    elif preset == "toon":
        diffuse = nodes.new(type="ShaderNodeBsdfDiffuse")
        diffuse.location = (250, 80)
        diffuse.inputs["Color"].default_value = base_color

        shader_to_rgb = nodes.new(type="ShaderNodeShaderToRGB")
        shader_to_rgb.location = (420, 80)

        ramp = nodes.new(type="ShaderNodeValToRGB")
        ramp.location = (580, 80)
        ramp.color_ramp.elements[0].position = 0.45
        ramp.color_ramp.elements[0].color = base_color
        ramp.color_ramp.elements[1].position = 0.55
        ramp.color_ramp.elements[1].color = accent_color

        principled = nodes.new(type="ShaderNodeBsdfPrincipled")
        principled.location = (580, -140)
        principled.inputs["Metallic"].default_value = max(0.0, min(metallic, 1.0))
        principled.inputs["Roughness"].default_value = max(0.0, min(roughness, 1.0))

        links.new(diffuse.outputs["BSDF"], shader_to_rgb.inputs["Shader"])
        links.new(shader_to_rgb.outputs["Color"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], principled.inputs["Base Color"])
        links.new(principled.outputs["BSDF"], out_node.inputs["Surface"])

    elif preset == "layered":
        base_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
        base_bsdf.location = (240, -120)
        base_bsdf.inputs["Base Color"].default_value = base_color
        base_bsdf.inputs["Metallic"].default_value = max(0.0, min(metallic, 1.0))
        base_bsdf.inputs["Roughness"].default_value = max(0.0, min(roughness, 1.0))

        clearcoat = nodes.new(type="ShaderNodeBsdfGlossy")
        clearcoat.location = (240, 120)
        clearcoat.inputs["Color"].default_value = accent_color
        clearcoat.inputs["Roughness"].default_value = max(
            0.0, min(roughness * 0.5, 1.0)
        )

        layer_mix = nodes.new(type="ShaderNodeMixShader")
        layer_mix.location = (470, 0)
        layer_mix.inputs["Fac"].default_value = max(0.0, min(mix_factor, 1.0))

        links.new(clearcoat.outputs["BSDF"], layer_mix.inputs[1])
        links.new(base_bsdf.outputs["BSDF"], layer_mix.inputs[2])
        links.new(layer_mix.outputs["Shader"], out_node.inputs["Surface"])

    else:
        raise ValueError(f"Unknown advanced material preset: {preset}")

    if len(obj.data.materials) == 0:
        obj.data.materials.append(material)
    else:
        obj.data.materials[0] = material

    return {
        "updated": object_name,
        "material": material_name,
        "preset": preset,
        "simulated": False,
    }
