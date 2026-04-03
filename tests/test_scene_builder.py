"""Phase-2 smoke tests around MCP bridge execution flow."""

import unittest

from core.mcp_bridge import MCPBridge
from core.validators import ToolCallValidator


class TestSceneBuilderFlow(unittest.TestCase):
    def test_bridge_execute_validated_tool(self):
        validator = ToolCallValidator()
        call_name = "create_cube"
        call_args = {
            "name": "UnitCube",
            "location": [0.0, 0.0, 0.0],
            "scale": [1.0, 1.0, 1.0],
        }

        valid = validator.validate(call_name, call_args)
        self.assertTrue(valid.valid)

        bridge = MCPBridge()
        try:
            init = bridge.initialize()
            self.assertIn("protocolVersion", init)
            result = bridge.call_tool(call_name, call_args)
            self.assertIn("content", result)
        finally:
            bridge.stop()


if __name__ == "__main__":
    unittest.main()
