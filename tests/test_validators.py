"""Unit tests for tool-call validation."""

import unittest

from core.validators import ToolCallValidator


class TestToolCallValidator(unittest.TestCase):
    def setUp(self):
        self.validator = ToolCallValidator()

    def test_valid_create_cube(self):
        result = self.validator.validate(
            "create_cube",
            {"name": "Cube", "location": [0.0, 0.0, 0.0], "scale": [1.0, 1.0, 1.0]},
        )
        self.assertTrue(result.valid)

    def test_unknown_tool(self):
        result = self.validator.validate("does_not_exist", {})
        self.assertFalse(result.valid)
        self.assertIn("Unknown tool", result.error or "")

    def test_required_fields(self):
        result = self.validator.validate("set_location", {"location": [0.0, 0.0, 0.0]})
        self.assertFalse(result.valid)
        self.assertIn("Missing required field", result.error or "")

    def test_additional_properties_rejected(self):
        result = self.validator.validate(
            "create_cube",
            {
                "name": "Cube",
                "location": [0.0, 0.0, 0.0],
                "scale": [1.0, 1.0, 1.0],
                "unexpected": 1,
            },
        )
        self.assertFalse(result.valid)
        self.assertIn("Unknown field", result.error or "")

    def test_array_shape_enforced(self):
        result = self.validator.validate(
            "create_cube", {"location": [0.0, 0.0], "scale": [1.0, 1.0, 1.0]}
        )
        self.assertFalse(result.valid)
        self.assertIn("at least", result.error or "")

    def test_advanced_material_preset_enum(self):
        result = self.validator.validate(
            "build_advanced_material_graph",
            {
                "object_name": "Cube",
                "preset": "nonexistent",
            },
        )
        self.assertFalse(result.valid)
        self.assertIn("must be one of", result.error or "")

    def test_advanced_material_valid(self):
        result = self.validator.validate(
            "build_advanced_material_graph",
            {
                "object_name": "Cube",
                "preset": "glass",
                "ior": 1.5,
            },
        )
        self.assertTrue(result.valid)

    def test_material_node_tool_required_fields(self):
        result = self.validator.validate(
            "add_material_node",
            {"material_name": "Mat"},
        )
        self.assertFalse(result.valid)
        self.assertIn("Missing required field", result.error or "")

    def test_material_vector_input_shape(self):
        result = self.validator.validate(
            "set_material_node_vector_input",
            {
                "material_name": "Mat",
                "node_name": "Mapping",
                "input_name": "Scale",
                "value": [1.0, 2.0],
            },
        )
        self.assertFalse(result.valid)
        self.assertIn("at least", result.error or "")

    def test_post_mvp_tools_exist(self):
        self.assertTrue(
            self.validator.validate("mesh_select_all", {"object_name": "Cube"}).valid
        )
        self.assertTrue(
            self.validator.validate("mesh_mark_seam", {"object_name": "Cube"}).valid
        )
        self.assertTrue(
            self.validator.validate("mesh_mark_sharp", {"object_name": "Cube"}).valid
        )
        self.assertTrue(
            self.validator.validate(
                "add_modifier",
                {"object_name": "Cube", "modifier_type": "SUBSURF"},
            ).valid
        )
        self.assertTrue(
            self.validator.validate("uv_unwrap", {"object_name": "Cube"}).valid
        )
        self.assertTrue(
            self.validator.validate(
                "create_texture_image",
                {"image_name": "PaintTex"},
            ).valid
        )


if __name__ == "__main__":
    unittest.main()
