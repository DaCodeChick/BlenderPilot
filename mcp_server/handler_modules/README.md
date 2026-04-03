# Handler Modules

This directory contains modular MCP tool handlers grouped by domain:

- `primitives.py`: primitive creation and transform handlers
- `materials.py`: material and shader graph handlers
- `scene.py`: camera/light/scene setup handlers
- `context.py`: shared Blender access helpers

`mcp_server/handlers.py` serves as a thin dispatcher compatibility layer.
