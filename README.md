# BlenderPilot

**AI-driven Blender automation via MCP (Model Context Protocol)**

BlenderPilot is a Blender 5.1+ addon that lets you create 3D models, materials, and scenes using natural language prompts. It uses the Model Context Protocol (MCP) to bridge AI models with Blender's powerful 3D tools.

---

## Features

- 🤖 **AI-Powered Generation**: Create 3D content from text prompts
- 🔧 **MCP Integration**: Clean, standardized protocol for AI-Blender communication  
- 🎨 **Multiple Providers**: Support for OpenAI and Anthropic (more coming soon)
- 🚀 **Easy Setup**: Auto-installs provider SDKs with Linux system package detection
- 🔐 **Secure**: API keys stored in Blender preferences or .env file
- 📦 **No Dependencies**: Bundles all required libraries

### Current Capabilities (MVP v0.1.0)

- **Modeling**: Primitives, transforms, modifiers
- **Materials**: Principled BSDF, shader graphs
- **Scene Setup**: Camera, lights, composition

### Coming Soon

- Image input (vision models)
- Advanced geometry nodes
- Sculpting automation
- Rigging and animation
- More AI providers

---

## Installation

### Requirements

- **Blender 5.1+** (Python 3.13+)
- **API Key** for OpenAI and/or Anthropic

### Method 1: Blender Extensions (Recommended)

1. Download `BlenderPilot-v0.1.0-extension.zip` from [Releases](https://github.com/yourusername/BlenderPilot/releases)
2. Open Blender 5.1+
3. Go to **Edit > Preferences > Get Extensions**
4. Click **Install from Disk** and select the downloaded zip
5. Enable the addon

### Method 2: Classic Addon

1. Download `BlenderPilot-v0.1.0.zip` from [Releases](https://github.com/yourusername/BlenderPilot/releases)
2. Open Blender 5.1+
3. Go to **Edit > Preferences > Add-ons**
4. Click **Install** and select the downloaded zip
5. Enable **BlenderPilot** in the addon list

---

## Quick Start

### 1. Configure API Keys

#### Option A: Blender Preferences (Recommended)

1. Go to **Edit > Preferences > Add-ons**
2. Find **BlenderPilot** and expand it
3. Enter your API keys:
   - **OpenAI**: Get from https://platform.openai.com/api-keys
   - **Anthropic**: Get from https://console.anthropic.com/
4. Select your preferred provider

#### Option B: .env File (Development)

1. Navigate to the addon directory:
   - Linux: `~/.config/blender/5.1/extensions/user_default/blenderpilot/`
   - Windows: `%APPDATA%\Blender Foundation\Blender\5.1\extensions\user_default\blenderpilot\`
   - macOS: `~/Library/Application Support/Blender/5.1/extensions/user_default/blenderpilot/`

2. Copy `.env.example` to `.env`
3. Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
BLENDERPILOT_DEFAULT_PROVIDER=openai
```

### 2. Open the Panel

1. Open Blender and switch to the **3D Viewport**
2. Press **N** to open the sidebar
3. Click the **BlenderPilot** tab

### 3. Generate Content

1. Enter a prompt, for example:
   - "Create a red cube"
   - "Add a sphere with a gold material"
   - "Create a table with 4 legs"
   - "Setup 3-point lighting"

2. Click **Generate**

3. Watch as BlenderPilot creates your content!

---

## Example Prompts

### Modeling

```
Create a simple house with walls, roof, and door
```

```
Add 5 cubes in a row, each slightly larger than the last
```

```
Make a chess board with alternating black and white squares
```

### Materials

```
Create a sphere with a metallic gold material
```

```
Add a glass material to the selected object
```

```
Make a glowing blue emissive material
```

### Scene Setup

```
Setup a 3-point lighting rig for product photography
```

```
Add a camera looking at the origin from 10 units away
```

```
Create a sunset lighting scene with warm colors
```

### Complex Prompts

```
Create a simple dining scene with a table, 4 chairs, and overhead lighting
```

```
Build a sci-fi corridor with metallic walls and blue accent lighting
```

---

## Configuration

### Provider Settings

BlenderPilot supports multiple AI providers. Configure them in **Preferences > Add-ons > BlenderPilot**:

| Provider | Pros | Best For |
|----------|------|----------|
| **OpenAI** | Most mature, strong tool calling | General use, structured output |
| **Anthropic** | Long context, strong reasoning | Complex scenes, detailed materials |

### Advanced Settings

- **Max Tokens**: Maximum length of AI responses (default: 4096)
- **Temperature**: Creativity level (0.0 = deterministic, 1.0 = creative, default: 0.7)
- **Auto-Install SDKs**: Automatically install provider SDKs if missing (default: on)

---

## Troubleshooting

### "No module named 'openai'" or "'anthropic'"

**Solution**: Enable **Auto-Install SDKs** in preferences, or manually install:

```bash
# Find Blender's Python
blender --background --python-expr "import sys; print(sys.executable)"

# Install SDKs
/path/to/blender/python -m pip install openai anthropic
```

### "Invalid API key"

**Solution**: 
1. Verify your API key is correct
2. Check you have credits/quota remaining
3. Ensure the key matches the selected provider

### "Connection timeout"

**Solution**:
1. Check your internet connection
2. Verify firewall isn't blocking Blender
3. Try a different provider

### Addon doesn't appear in sidebar

**Solution**:
1. Press **N** in the 3D Viewport to open sidebar
2. Look for the **BlenderPilot** tab
3. If missing, check addon is enabled in Preferences

---

## Development

### Project Structure

```
BlenderPilot/
├── blender_manifest.toml      # Extension manifest
├── __init__.py                # Main addon entry point
├── core/                      # Pure Python logic
│   ├── provider_interface.py # AI provider abstraction
│   ├── sdk_installer.py      # Auto-install SDKs
│   └── providers/            # Provider implementations
├── mcp_server/               # MCP server subprocess
│   ├── main.py              # Server entry point
│   ├── tool_definitions/    # Modular MCP tool schemas
│   └── handler_modules/     # Modular tool handlers
├── ops/                     # Blender operators
├── ui/                      # UI panels
├── props/                   # Property groups
└── tests/                   # Unit tests
```

### Running Tests

If `pytest` is installed:

```bash
python -m pytest tests/
```

Or run built-in unittest (no extra dependency):

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Building from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/BlenderPilot.git
cd BlenderPilot
```

2. Install development dependencies:
```bash
pip install -r requirements.txt
```

3. Create distribution packages:
```bash
./scripts/package_release.sh 0.1.0
```

Artifacts are written to `dist/`.

4. Verify release artifacts and tests:
```bash
./scripts/verify_release.sh
```

### Release Checklist

- Update `CHANGELOG.md`
- Run `./scripts/verify_release.sh`
- Build artifacts with `./scripts/package_release.sh <version>`
- Tag and publish release

---

## Architecture

### MCP Integration

BlenderPilot uses the **Model Context Protocol (MCP)** to standardize communication between AI models and Blender:

```
User Prompt → AI Provider → MCP Tool Calls → Blender Operations
```

**Why MCP?**
- **Standardized**: Works with any MCP-compatible AI model
- **Safe**: Validates all operations before execution
- **Extensible**: Easy to add new tools and capabilities
- **Transparent**: Clear separation between AI decisions and Blender execution

### Provider Abstraction

BlenderPilot uses a provider-agnostic interface, making it easy to add new AI services:

```python
class ProviderInterface(ABC):
    def generate_tool_calls(self, prompt, available_tools) -> ProviderResponse:
        """Convert prompt to MCP tool calls"""
        pass
```

Current providers:
- OpenAI (GPT-4, GPT-4 Turbo)
- Anthropic (Claude 3)

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- **New Providers**: Add support for Gemini, Groq, local models, etc.
- **MCP Tools**: Implement more Blender operations
- **UI Improvements**: Better status, history, undo/redo
- **Documentation**: Tutorials, examples, videos
- **Testing**: More test coverage

---

## License

BlenderPilot is licensed under the **GNU General Public License v3.0 or later**.

See [LICENSE](LICENSE) for details.

---

## Credits

**Created by**: BlenderPilot Contributors  
**MCP Protocol**: Anthropic  
**Blender**: Blender Foundation

### Third-Party Dependencies

- `openai` - OpenAI Python SDK (MIT License)
- `anthropic` - Anthropic Python SDK (MIT License)
- `mcp` - Model Context Protocol SDK (MIT License)

---

## Links

- **GitHub**: https://github.com/yourusername/BlenderPilot
- **Issues**: https://github.com/yourusername/BlenderPilot/issues
- **Discussions**: https://github.com/yourusername/BlenderPilot/discussions
- **MCP Spec**: https://spec.modelcontextprotocol.io/

---

## Changelog

### v0.1.0 (2026-04-03)

**Initial MVP Release**

- ✅ Basic text prompt support
- ✅ OpenAI and Anthropic providers
- ✅ Primitive modeling tools
- ✅ Basic material setup
- ✅ Scene lighting and camera
- ✅ Auto-install SDKs
- ✅ Linux system package detection

**Coming in v0.2.0**:
- Image input (vision models)
- Advanced shader graphs
- More MCP tools
- Prompt history

---

*Made with ❤️ for the Blender community*
