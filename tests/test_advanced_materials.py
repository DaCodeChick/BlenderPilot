"""Tests for advanced material graph handler availability."""

import unittest

from mcp_server.handler_modules import HANDLERS


class TestAdvancedMaterials(unittest.TestCase):
    def test_handler_registered(self):
        self.assertIn("build_advanced_material_graph", HANDLERS)

    def test_simulated_execution(self):
        result = HANDLERS["build_advanced_material_graph"](
            {
                "object_name": "Cube",
                "preset": "emissive",
                "material_name": "Glow",
            }
        )
        self.assertIn("updated", result)
        self.assertIn("preset", result)


if __name__ == "__main__":
    unittest.main()
