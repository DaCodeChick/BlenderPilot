# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-04-03

### Added
- Phase 1 foundation addon scaffold, UI panels, preferences, and core abstractions.
- MCP subprocess bridge and local stdio JSON-RPC server.
- MCP tool catalog for primitives, transforms, materials, and scene setup.
- OpenAI and Anthropic provider adapters with tool-calling support.
- Unit test suite for validators, provider behavior, bridge flow, installer, and protocol checks.
- Release packaging script at `scripts/package_release.sh`.

### Changed
- Refactored MCP schemas into modular files under `mcp_server/tool_definitions/`.
- Refactored MCP handlers into modular files under `mcp_server/handler_modules/`.
- Hardened generation flow with retry/backoff and clearer user-facing error messages.

### Removed
- Transitional MCP wrapper files (`mcp_server/tools.py`, `mcp_server/handlers.py`).
