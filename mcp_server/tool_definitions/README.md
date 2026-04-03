# Tool Definition Modules

This directory contains modular MCP tool schema catalogs grouped by domain:

- `primitives.py`: primitive and grouped primitive tools
- `transforms.py`: transform tools
- `materials.py`: material tools
- `scene.py`: camera/light/scene tools
- `schema.py`: shared schema builders

`mcp_server/tools.py` re-exports the combined catalog for backward compatibility.
