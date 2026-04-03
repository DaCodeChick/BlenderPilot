"""Composable MCP handler registry."""

from .materials import (
    add_material_node,
    apply_material,
    build_advanced_material_graph,
    build_material_graph,
    connect_material_nodes,
    set_material_node_color_input,
    set_material_node_float_input,
    set_material_node_texture_image,
    set_material_node_vector_input,
)
from .mesh_edit import (
    mesh_bevel,
    mesh_extrude_region,
    mesh_inset,
    mesh_mark_seam,
    mesh_mark_sharp,
    mesh_select_all,
)
from .modifiers import add_modifier, apply_modifier, configure_modifier
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
from .texture_paint import assign_texture_paint_image, create_texture_image
from .uv import uv_smart_project, uv_unwrap


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
    "mesh_select_all": mesh_select_all,
    "mesh_extrude_region": mesh_extrude_region,
    "mesh_bevel": mesh_bevel,
    "mesh_inset": mesh_inset,
    "mesh_mark_seam": mesh_mark_seam,
    "mesh_mark_sharp": mesh_mark_sharp,
    "add_modifier": add_modifier,
    "configure_modifier": configure_modifier,
    "apply_modifier": apply_modifier,
    "uv_unwrap": uv_unwrap,
    "uv_smart_project": uv_smart_project,
    "create_texture_image": create_texture_image,
    "assign_texture_paint_image": assign_texture_paint_image,
    "apply_material": apply_material,
    "build_material_graph": build_material_graph,
    "build_advanced_material_graph": build_advanced_material_graph,
    "add_material_node": add_material_node,
    "connect_material_nodes": connect_material_nodes,
    "set_material_node_float_input": set_material_node_float_input,
    "set_material_node_color_input": set_material_node_color_input,
    "set_material_node_vector_input": set_material_node_vector_input,
    "set_material_node_texture_image": set_material_node_texture_image,
    "create_light": create_light,
    "create_camera": create_camera,
    "setup_scene": setup_scene,
}
