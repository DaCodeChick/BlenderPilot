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


if __name__ == "__main__":
    unittest.main()
