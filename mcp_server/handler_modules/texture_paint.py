"""Texture painting handlers."""

from __future__ import annotations

from typing import Any, Dict

from .context import CTX, bpy


def create_texture_image(args: Dict[str, Any]) -> Dict[str, Any]:
    image_name = args["image_name"]
    width = int(args.get("width", 1024))
    height = int(args.get("height", 1024))
    color = args.get("color", [1.0, 1.0, 1.0, 1.0])
    alpha = bool(args.get("alpha", True))

    if not CTX.available:
        return {
            "image": image_name,
            "size": [width, height],
            "simulated": True,
        }

    image = bpy.data.images.new(
        name=image_name,
        width=max(1, width),
        height=max(1, height),
        alpha=alpha,
    )
    image.generated_color = color
    return {
        "image": image.name,
        "size": [image.size[0], image.size[1]],
        "simulated": False,
    }


def assign_texture_paint_image(args: Dict[str, Any]) -> Dict[str, Any]:
    material_name = args["material_name"]
    node_name = args["node_name"]
    image_name = args["image_name"]

    if not CTX.available:
        return {
            "material": material_name,
            "node": node_name,
            "image": image_name,
            "simulated": True,
        }

    material = bpy.data.materials.get(material_name)
    if material is None:
        raise ValueError(f"Material not found: {material_name}")
    if not material.node_tree:
        raise ValueError(f"Material node tree unavailable: {material_name}")

    node = material.node_tree.nodes.get(node_name)
    if node is None:
        raise ValueError(f"Node not found: {node_name}")
    if node.bl_idname != "ShaderNodeTexImage":
        raise ValueError(f"Node is not an Image Texture node: {node_name}")

    image = bpy.data.images.get(image_name)
    if image is None:
        raise ValueError(f"Image not found: {image_name}")

    node.image = image
    return {
        "material": material_name,
        "node": node_name,
        "image": image.name,
        "simulated": False,
    }
