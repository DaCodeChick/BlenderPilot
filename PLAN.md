# BlenderPilot Implementation Plan

## Executive Summary

BlenderPilot is a Blender 5.1+ addon that provides AI-driven 3D automation through an embedded MCP (Model Context Protocol) server. Users enter text prompts in a sidebar panel; the AI calls MCP tools to create models, materials, and scene setups.

**Target Release:** v0.1.0 MVP  
**License:** GPL-3.0  
**Blender Version:** 5.1+  
**Python Version:** 3.13+ (compatible with 3.14)

---

## Architecture

### High-Level Flow

```
User Prompt (N-panel)
    ↓
AI Provider (OpenAI/Anthropic)
    ↓
MCP Tool Calls (JSON-RPC)
    ↓
MCP Server (subprocess, stdio)
    ↓
Tool Handlers → Blender Operations
    ↓
Scene Updated
```

### Component Layers

1. **UI Layer** - Blender addon N-panel in 3D View
2. **Core Logic** - Pure Python, no `bpy` dependencies
3. **MCP Server** - Subprocess with stdio transport
4. **AI Provider Adapters** - OpenAI and Anthropic implementations
5. **Blender Operations** - Safe `bpy` execution on main thread

### Key Design Decisions

- ✅ **MCP server as subprocess** - Clean stdio, process isolation
- ✅ **AI uses MCP tool calling** - Not JSON schema or code generation
- ✅ **Hybrid tool granularity** - Atomic for common ops, batch for workflows
- ✅ **Auto-install SDKs** - With Linux system package detection
- ✅ **OpenAI + Anthropic** - For MVP providers
- ✅ **Strict validation, fail fast** - For errors
- ✅ **Unit tests + manual testing**
- ✅ **Blender 5.1+ only**
- ✅ **Both .zip and Extension formats** - For distribution

---

## Directory Structure

```
BlenderPilot/
├── blender_manifest.toml          # Blender 5.1 extension manifest
├── __init__.py                    # Addon registration
├── README.md                      # User documentation
├── PLAN.md                        # This file
├── .env.example                   # API key template
├── requirements.txt               # Dev dependencies (not bundled)
├── .gitignore                     # Already exists
├── LICENSE                        # Already exists (GPL-3.0)
│
├── core/                          # Pure logic (no bpy)
│   ├── __init__.py
│   ├── mcp_bridge.py             # MCP subprocess manager
│   ├── provider_interface.py     # AI provider abstraction
│   ├── providers/                # Provider implementations
│   │   ├── __init__.py
│   │   ├── openai_provider.py
│   │   └── anthropic_provider.py
│   ├── scene_builder.py          # Apply tool calls to Blender
│   ├── validators.py             # JSON schema validation
│   └── sdk_installer.py          # Auto-install provider SDKs
│
├── mcp_server/                    # MCP server subprocess
│   ├── __init__.py
│   ├── main.py                   # Entry point for subprocess
│   ├── tools.py                  # MCP tool definitions
│   └── handlers.py               # Tool execution handlers
│
├── ops/                           # Blender operators
│   ├── __init__.py
│   ├── generate.py               # Main generation operator
│   └── utils.py                  # Operator helpers
│
├── ui/                            # UI panels
│   ├── __init__.py
│   ├── panels.py                 # N-panel definitions
│   └── icons.py                  # Icon management
│
├── props/                         # Property groups
│   ├── __init__.py
│   ├── scene_props.py            # Scene-level properties
│   └── preferences.py            # Addon preferences
│
├── vendor/                        # Bundled dependencies
│   └── mcp/                      # Official MCP SDK (vendored)
│
└── tests/                         # Unit tests
    ├── __init__.py
    ├── test_providers.py
    ├── test_validators.py
    └── test_scene_builder.py
```

---

## Technology Stack

### Core Dependencies (Bundled)

- `mcp` (official Python SDK) - Vendored in `vendor/`
- `pydantic` - For validation (already dep of `mcp`)
- `python-dotenv` - For `.env` loading

### Provider SDKs (Auto-installed, not bundled)

- `openai` - Primary provider
- `anthropic` - Secondary provider

**Installation Strategy:**
1. Check if already importable (system or Blender Python)
2. On Linux: check system packages first, add to sys.path if available
3. Auto-install to Blender's Python as fallback

### Blender Requirements

- **Blender:** 5.1+
- **Python:** 3.13+ (bundled with Blender)
- **Blender APIs:** `bpy`, `bpy.types`, `bpy.props`, `bpy.utils`

---

## MCP Tool Catalog (Hybrid Granularity)

### Atomic Tools (Common Operations)

**Primitives:**
- `create_cube` - Create a cube mesh
- `create_sphere` - Create a UV sphere
- `create_cylinder` - Create a cylinder
- `create_cone` - Create a cone
- `create_torus` - Create a torus
- `create_plane` - Create a plane

**Transforms:**
- `set_location` - Set object location
- `set_rotation` - Set object rotation
- `set_scale` - Set object scale

**Materials:**
- `apply_material` - Apply material to object

**Scene:**
- `create_light` - Create a light (sun, point, spot, area)
- `create_camera` - Create a camera

### Batch Tools (Complex Workflows)

- `create_primitive_group` - Create multiple primitives with transforms
- `build_material_graph` - Create shader nodes + connections
- `setup_scene` - Camera + lights + environment in one call

### Tool Schema Example

```json
{
  "name": "create_cube",
  "description": "Create a cube mesh primitive",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "default": "Cube",
        "description": "Name of the cube object"
      },
      "location": {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 3,
        "maxItems": 3,
        "default": [0, 0, 0],
        "description": "XYZ location"
      },
      "scale": {
        "type": "array",
        "items": {"type": "number"},
        "minItems": 3,
        "maxItems": 3,
        "default": [1, 1, 1],
        "description": "XYZ scale"
      }
    }
  }
}
```

---

## AI Provider Integration

### Provider Interface

```python
class ProviderInterface(ABC):
    @abstractmethod
    def generate_tool_calls(self, prompt: str, available_tools: list) -> list[ToolCall]:
        """Returns list of MCP tool calls from AI"""
        pass
    
    @abstractmethod
    def supports_vision(self) -> bool:
        """Whether provider supports image input (Phase 2)"""
        pass
```

### Supported Providers (MVP)

| Provider | SDK | Auth | Streaming | Vision (Phase 2) |
|----------|-----|------|-----------|------------------|
| OpenAI | `openai` | `OPENAI_API_KEY` | Yes | Yes (GPT-4V) |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` | Yes | Yes (Claude 3) |

### Configuration

**Development (.env):**
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
BLENDERPILOT_DEFAULT_PROVIDER=openai
```

**Production (Addon Preferences):**
- API keys stored in Blender preferences
- Provider selection dropdown
- Advanced settings (temperature, max tokens, etc.)

---

## Error Handling Strategy

### Strict Validation, Fail Fast

```python
class ToolCallValidator:
    def validate(self, tool_name: str, args: dict) -> Result:
        # 1. Tool exists?
        # 2. Args match schema?
        # 3. Blender objects exist? (if referencing names)
        # 4. Values in valid ranges?
        
        if not valid:
            return Error("Invalid tool call: ...")
        
        return Ok(args)
```

### Failure Modes

- ❌ Invalid tool call → Show error, don't execute
- ❌ Invalid args → Show error, don't execute
- ❌ Missing object → Show error, don't execute
- ✅ Valid → Execute on main thread, show success

### User Feedback

- Clear error messages in UI
- Suggest prompt improvements
- Log AI responses for debugging (stderr)

---

## Implementation Phases

### Phase 1: Foundation (Week 1-2)

**Goal:** Addon scaffold, UI, preferences, SDK installation

**Deliverables:**
1. Addon scaffold with `blender_manifest.toml`
2. N-panel UI (text input, provider selector, generate button)
3. Addon preferences (API keys)
4. SDK installer (auto-install with Linux detection)
5. Basic provider abstraction (OpenAI + Anthropic)

**Files to Create:**
- `blender_manifest.toml`
- `__init__.py` (registration)
- `ui/panels.py` (N-panel)
- `props/preferences.py` (API keys)
- `props/scene_props.py` (UI state)
- `core/sdk_installer.py`
- `core/provider_interface.py`
- `core/providers/openai_provider.py`
- `core/providers/anthropic_provider.py`
- `.env.example`

---

### Phase 2: MCP Server (Week 2-3)

**Goal:** MCP server subprocess, tool catalog, handlers

**Deliverables:**
1. MCP server subprocess manager
2. stdio JSON-RPC communication
3. Initial MCP tool catalog (10-15 tools)
4. Tool handlers (execute Blender ops)
5. Validation layer

**Files to Create:**
- `core/mcp_bridge.py` (subprocess manager)
- `mcp_server/main.py` (server entry point)
- `mcp_server/tools.py` (tool definitions)
- `mcp_server/handlers.py` (tool execution)
- `core/validators.py`
- `vendor/mcp/` (vendored SDK)

**Sample Tools:**
- Primitives: `create_cube`, `create_sphere`, `create_cylinder`, `create_cone`, `create_torus`, `create_plane`
- Transforms: `set_location`, `set_rotation`, `set_scale`
- Materials: `apply_material`, `build_material_graph`
- Scene: `create_camera`, `create_light`, `setup_scene`
- Batch: `create_primitive_group`

---

### Phase 3: AI Integration (Week 3-4)

**Goal:** Provider implementations, tool calling, main operator

**Deliverables:**
1. Provider implementations (OpenAI, Anthropic)
2. Tool calling prompts
3. Response parsing
4. Main generation operator
5. Progress/status UI

**Files to Create:**
- `ops/generate.py` (main operator)
- `core/scene_builder.py` (apply tool calls to scene)
- Tool calling system prompts

**Workflow:**
1. User enters prompt: "Create a table with 4 legs and a wood material"
2. Addon calls provider: `generate_tool_calls(prompt)`
3. AI returns: `[create_primitive_group(...), build_material_graph(...)]`
4. Addon validates tool calls
5. Addon executes handlers on main thread
6. Scene updated, status shown

---

### Phase 4: Testing & Polish (Week 4-5)

**Goal:** Tests, documentation, packaging

**Deliverables:**
1. Unit tests (provider abstraction, validators)
2. Integration tests (manual Blender testing)
3. Error handling improvements
4. Documentation (README, .env.example)
5. Distribution packaging (zip + extension)

**Files to Create:**
- `tests/test_providers.py`
- `tests/test_validators.py`
- `tests/test_scene_builder.py`
- `README.md`
- `requirements.txt` (dev dependencies)
- Release packaging scripts

---

### Phase 5: MVP Release (Week 5-6)

**Goal:** GitHub Release v0.1.0

**Deliverables:**
1. GitHub Release (v0.1.0)
2. User documentation
3. Demo video/screenshots
4. Issue templates

**Release Checklist:**
- [ ] Version bump in manifest
- [ ] Changelog updated
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Demo assets included
- [ ] Create release tag
- [ ] Upload both formats (zip + extension)
- [ ] Announce on Blender forums/Reddit

---

## MVP Feature Scope

### ✅ Included in MVP

**Modeling:**
- Primitives (cube, sphere, cylinder, cone, torus, plane)
- Basic mesh operations (scale, rotate, translate)
- Array/mirror modifiers
- Boolean operations
- Simple geometry nodes setup

**Materials:**
- Principled BSDF configuration
- Basic shader node setup (color, roughness, metallic)
- Simple node groups
- Texture coordinate mapping

**Scene Setup:**
- Camera positioning
- Light creation/configuration (sun, point, area, spot)
- Basic scene composition

**UI:**
- N-panel in 3D View sidebar
- Provider selection dropdown
- API key configuration (preferences)
- Text prompt input
- Generate button
- Status/progress indicator
- Error display

### ❌ Post-MVP (Phase 2+)

- Image input (vision models)
- Advanced shader graphs
- Sculpting automation
- Rigging setup
- Animation keyframing
- More providers (Gemini, Groq, OpenRouter)
- Prompt history
- Undo/redo integration
- Batch operations
- Custom tool plugins

---

## Distribution Strategy

### GitHub Releases

**Two Formats:**

1. **Zip Archive** (`BlenderPilot-v0.1.0.zip`)
   - Classic addon format
   - Manual install via Blender Preferences > Add-ons > Install

2. **Blender Extension** (`BlenderPilot-v0.1.0-extension.zip`)
   - Modern Extensions format with `blender_manifest.toml`
   - Install via Blender Extensions system

### Release Process

1. Version bump in `blender_manifest.toml`
2. Update CHANGELOG.md
3. Run tests
4. Create git tag: `git tag -a v0.1.0 -m "Release v0.1.0"`
5. Push tag: `git push origin v0.1.0`
6. Build both distribution formats
7. Create GitHub Release with both assets
8. Update README with installation instructions

---

## Testing Strategy

### Unit Tests

**Target Coverage:**
- Provider abstraction
- Validators
- Scene builder logic
- SDK installer

**Framework:** Python `unittest` or `pytest`

**Run:** `python -m pytest tests/`

### Integration Tests

**Manual Testing in Blender:**
- Load addon in Blender 5.1+
- Test each tool individually
- Test complex prompts
- Test error cases
- Test on Linux/Windows/macOS

**Test Prompts:**
- "Create a red cube"
- "Add a sphere with a gold material"
- "Create a table with 4 legs"
- "Setup a 3-point lighting rig"
- "Build a simple house scene"

---

## Documentation Plan

### README.md

**Sections:**
1. Overview & features
2. Installation
   - Classic addon format
   - Extension format
3. Quick start
4. API key setup
5. Supported providers
6. Example prompts
7. Troubleshooting
8. Contributing
9. License

### In-Addon Help

- Tooltip on every UI element
- Link to docs in preferences
- Example prompt suggestions in panel

### .env.example

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Default Provider (openai or anthropic)
BLENDERPILOT_DEFAULT_PROVIDER=openai
```

---

## Technical Specifications

### Blender Manifest

```toml
schema_version = "1.0.0"
id = "blenderpilot"
version = "0.1.0"
name = "BlenderPilot"
tagline = "AI-driven Blender automation via MCP"
maintainer = "Your Name <email@example.com>"
type = "add-on"
tags = ["3D View", "AI", "Automation"]
blender_version_min = "5.1.0"
license = ["SPDX:GPL-3.0-or-later"]

[permissions]
network = "Access AI provider APIs"
files = "Read .env configuration"
```

### bl_info (for classic addon)

```python
bl_info = {
    "name": "BlenderPilot",
    "author": "Your Name",
    "version": (0, 1, 0),
    "blender": (5, 1, 0),
    "location": "View3D > Sidebar > BlenderPilot",
    "description": "AI-driven Blender automation via MCP",
    "category": "3D View",
}
```

---

## Security & Safety

### API Key Management

- Store in Blender preferences (not in blend files)
- Support .env for development
- Never commit keys to git (.gitignore)
- Validate keys before use

### Tool Execution Safety

- Validate all tool calls before execution
- Sandbox tool execution (no file system access)
- Limit object creation (prevent infinite loops)
- User confirmation for destructive operations

### Network Safety

- HTTPS only for API calls
- Timeout on all network requests
- Handle rate limits gracefully
- No telemetry without user consent

---

## Performance Considerations

### Main Thread Safety

- All `bpy` operations on main thread
- Use `bpy.app.timers` for async callbacks
- Modal operators for long-running tasks

### MCP Server Performance

- Subprocess isolation prevents Blender freezing
- stdio transport is lightweight
- Tool validation happens before execution

### AI Provider Optimization

- Stream responses when possible
- Cache tool schemas
- Batch tool calls when feasible
- Implement request timeouts

---

## Known Limitations & Future Work

### MVP Limitations

- Text prompts only (no image input)
- Limited to basic modeling/materials
- No undo/redo integration
- No prompt history
- Two providers only (OpenAI, Anthropic)

### Future Enhancements

1. **Image Input** (Phase 2)
   - Vision model support
   - Image-to-3D workflows
   - Reference image analysis

2. **Advanced Automation** (Phase 3)
   - Sculpting tools
   - Rigging automation
   - Animation keyframing
   - Geometry nodes templates

3. **User Experience** (Phase 4)
   - Prompt history/favorites
   - Undo/redo integration
   - Batch operations
   - Custom tool plugins

4. **More Providers** (Phase 5)
   - Google Gemini
   - Groq (fast inference)
   - OpenRouter (multi-model)
   - Local models (Ollama)

---

## Questions & Decisions Log

### Answered Questions

1. **Provider SDK Installation?** → Auto-install with Linux system package detection
2. **Initial Provider Support?** → OpenAI + Anthropic
3. **Prompt Engineering Approach?** → MCP tool calling
4. **Error Handling Strategy?** → Strict validation, fail fast
5. **Testing Strategy?** → Unit tests + manual testing
6. **Tool Granularity?** → Hybrid (atomic + batch)
7. **Blender Version Support?** → Blender 5.1+ only
8. **Distribution Format?** → Both zip and extension

### Open Questions

- Exact system prompt for tool calling
- Tool call batching strategy
- Rate limit handling approach
- Telemetry/analytics (none for MVP)

---

## Resources & References

### Official Documentation

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Blender 5.1 Python API](https://docs.blender.org/api/5.1/)
- [Blender Extensions](https://docs.blender.org/manual/en/latest/extensions/)

### AI Provider APIs

- [OpenAI API](https://platform.openai.com/docs/)
- [Anthropic API](https://docs.anthropic.com/)

### Community

- [Blender Artists Forum](https://blenderartists.org/)
- [r/blender](https://reddit.com/r/blender)
- [Blender Stack Exchange](https://blender.stackexchange.com/)

---

## License

GPL-3.0 (inherited from repository)

---

## Contact & Contribution

**Repository:** https://github.com/yourusername/BlenderPilot  
**Issues:** https://github.com/yourusername/BlenderPilot/issues  
**Discussions:** https://github.com/yourusername/BlenderPilot/discussions

---

*Last Updated: 2026-04-03*
