# BlenderPilot - AI-driven Blender automation via MCP
# Copyright (C) 2026 BlenderPilot Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""
BlenderPilot - AI-driven Blender automation via MCP

This addon provides an MCP (Model Context Protocol) bridge that allows AI models
to control Blender through tool calling. Users enter text prompts, and the AI
generates appropriate MCP tool calls to create 3D models, materials, and scenes.
"""

bl_info = {
    "name": "BlenderPilot",
    "author": "BlenderPilot Contributors",
    "version": (0, 1, 0),
    "blender": (5, 1, 0),
    "location": "View3D > Sidebar > BlenderPilot",
    "description": "AI-driven Blender automation via MCP",
    "warning": "Early development version",
    "doc_url": "https://github.com/yourusername/BlenderPilot",
    "tracker_url": "https://github.com/yourusername/BlenderPilot/issues",
    "category": "3D View",
}


# Module imports
import bpy
import sys
from pathlib import Path


# Add vendor directory to path for bundled dependencies
addon_dir = Path(__file__).parent
vendor_dir = addon_dir / "vendor"
if vendor_dir.exists() and str(vendor_dir) not in sys.path:
    sys.path.insert(0, str(vendor_dir))


# Import submodules
from . import props
from . import ui
from . import ops


# Module list for registration
modules = (
    props.preferences,
    props.scene_props,
    ui.panels,
    ops.generate,
)


def register():
    """Register all addon components."""
    # Register all modules
    for module in modules:
        if hasattr(module, "register"):
            module.register()

    print("BlenderPilot: Addon registered successfully")


def unregister():
    """Unregister all addon components."""
    # Unregister in reverse order
    for module in reversed(modules):
        if hasattr(module, "unregister"):
            module.unregister()

    print("BlenderPilot: Addon unregistered")


if __name__ == "__main__":
    register()
