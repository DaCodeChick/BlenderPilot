"""Tests for low-level material node graph tools."""

import unittest

from mcp_server.handler_modules import HANDLERS


class TestMaterialNodeTools(unittest.TestCase):
    def test_handlers_registered(self):
        self.assertIn("add_material_node", HANDLERS)
        self.assertIn("connect_material_nodes", HANDLERS)
        self.assertIn("set_material_node_float_input", HANDLERS)
        self.assertIn("set_material_node_color_input", HANDLERS)
        self.assertIn("set_material_node_vector_input", HANDLERS)
        self.assertIn("set_material_node_texture_image", HANDLERS)

    def test_add_node_simulated(self):
        result = HANDLERS["add_material_node"](
            {
                "material_name": "Mat",
                "node_type": "ShaderNodeTexNoise",
                "node_name": "Noise",
                "location": [0.0, 0.0],
            }
        )
        self.assertIn("material", result)
        self.assertIn("node_name", result)

    def test_connect_nodes_simulated(self):
        result = HANDLERS["connect_material_nodes"](
            {
                "material_name": "Mat",
                "from_node": "Noise",
                "from_socket": "Color",
                "to_node": "Principled BSDF",
                "to_socket": "Base Color",
            }
        )
        self.assertIn("from", result)
        self.assertIn("to", result)

    def test_vector_input_simulated(self):
        result = HANDLERS["set_material_node_vector_input"](
            {
                "material_name": "Mat",
                "node_name": "Mapping",
                "input_name": "Scale",
                "value": [1.0, 2.0, 3.0],
            }
        )
        self.assertEqual(result["value"], [1.0, 2.0, 3.0])

    def test_texture_image_simulated(self):
        result = HANDLERS["set_material_node_texture_image"](
            {
                "material_name": "Mat",
                "node_name": "Image Texture",
                "image_path": "/tmp/fake.png",
                "colorspace": "Non-Color",
            }
        )
        self.assertEqual(result["colorspace"], "Non-Color")


if __name__ == "__main__":
    unittest.main()
