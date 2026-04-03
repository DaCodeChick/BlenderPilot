"""Composable MCP handler registry."""

from .materials import (
    add_material_node,
    apply_material,
    build_advanced_material_graph,
    build_material_graph,
    connect_material_nodes,
    set_material_node_color_input,
    set_material_node_float_input,
)
from .primitives import (
    create_cone,
    create_cube,
    create_cylinder,
    create_plane,
    create_primitive_group,
    create_sphere,
    create_torus,
    set_location,
    set_rotation,
    set_scale,
)
from .scene import create_camera, create_light, setup_scene


HANDLERS = {
    "create_cube": create_cube,
    "create_sphere": create_sphere,
    "create_cylinder": create_cylinder,
    "create_cone": create_cone,
    "create_torus": create_torus,
    "create_plane": create_plane,
    "create_primitive_group": create_primitive_group,
    "set_location": set_location,
    "set_rotation": set_rotation,
    "set_scale": set_scale,
    "apply_material": apply_material,
    "build_material_graph": build_material_graph,
    "build_advanced_material_graph": build_advanced_material_graph,
    "add_material_node": add_material_node,
    "connect_material_nodes": connect_material_nodes,
    "set_material_node_float_input": set_material_node_float_input,
    "set_material_node_color_input": set_material_node_color_input,
    "create_light": create_light,
    "create_camera": create_camera,
    "setup_scene": setup_scene,
}
