"""Tests for post-MVP mesh/modifier/UV/texture tool registration and simulated execution."""

import unittest

from mcp_server.handler_modules import HANDLERS


class TestPostMVPMeshTools(unittest.TestCase):
    def test_mesh_tools_registered(self):
        self.assertIn("mesh_select_all", HANDLERS)
        self.assertIn("mesh_extrude_region", HANDLERS)
        self.assertIn("mesh_bevel", HANDLERS)
        self.assertIn("mesh_inset", HANDLERS)
        self.assertIn("mesh_mark_seam", HANDLERS)
        self.assertIn("mesh_mark_sharp", HANDLERS)

    def test_mesh_select_all_simulated(self):
        res = HANDLERS["mesh_select_all"]({"object_name": "Cube", "action": "SELECT"})
        self.assertTrue(res["simulated"])

    def test_mesh_mark_tools_simulated(self):
        seam = HANDLERS["mesh_mark_seam"]({"object_name": "Cube", "clear": False})
        sharp = HANDLERS["mesh_mark_sharp"]({"object_name": "Cube", "clear": True})
        self.assertTrue(seam["simulated"])
        self.assertTrue(sharp["simulated"])


class TestPostMVPModifierTools(unittest.TestCase):
    def test_modifier_tools_registered(self):
        self.assertIn("add_modifier", HANDLERS)
        self.assertIn("configure_modifier", HANDLERS)
        self.assertIn("apply_modifier", HANDLERS)

    def test_add_modifier_simulated(self):
        res = HANDLERS["add_modifier"](
            {
                "object_name": "Cube",
                "modifier_type": "SUBSURF",
                "modifier_name": "Subsurf",
            }
        )
        self.assertTrue(res["simulated"])


class TestPostMVPUVTools(unittest.TestCase):
    def test_uv_tools_registered(self):
        self.assertIn("uv_unwrap", HANDLERS)
        self.assertIn("uv_smart_project", HANDLERS)

    def test_uv_unwrap_simulated(self):
        res = HANDLERS["uv_unwrap"]({"object_name": "Cube", "method": "ANGLE_BASED"})
        self.assertTrue(res["simulated"])


class TestPostMVPTextureTools(unittest.TestCase):
    def test_texture_tools_registered(self):
        self.assertIn("create_texture_image", HANDLERS)
        self.assertIn("assign_texture_paint_image", HANDLERS)

    def test_texture_create_simulated(self):
        res = HANDLERS["create_texture_image"](
            {
                "image_name": "PaintTex",
                "width": 512,
                "height": 512,
            }
        )
        self.assertTrue(res["simulated"])


if __name__ == "__main__":
    unittest.main()
